from django.shortcuts import render
from . import util
from django import forms
import markdown2
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

class SearchForm(forms.Form):
    search = forms.CharField(label="Search")

class newpageform(forms.Form):
    page_title=forms.CharField(label="Title")
    page_content= forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 200px;width:500px'}))

class editform(forms.Form):
    content=forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 200px;width:500px','value':''}),label="Content")

entries1=util.list_entries()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def title(request,title):
    entry=util.get_entry(title)
    if entry is None:
        return render(request,"encyclopedia/error.html")
    else:
        return render(request,"encyclopedia/entry.html",{
            "content":  markdown2.markdown(util.get_entry(title)),"form": SearchForm(),"title":title
        })


def search(request):
    if request.method=="POST":
        entries2=[]
        counter=0
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]



            if search in entries1:
                return render(request, "encyclopedia/entry.html", {"content": markdown2.markdown(util.get_entry(search)),"form": SearchForm(),"title":search})
            else:
                for entry in entries1:
                    if search in entry:
                        entries2.append(entry)
                        counter+=1
                if counter>0:
                    return render(request,"encyclopedia/search.html",{"results": entries2,"form": SearchForm()})
                else:
                    return render(request, "encyclopedia/error.html")

def newpage(request):
    if request.method=="GET":
        return render(request,"encyclopedia/newpage.html",{"newpageform":newpageform(),"form": SearchForm()})
    else:
        form=newpageform(request.POST)
        if form.is_valid():
            page_title=form.cleaned_data["page_title"]
            page_content=form.cleaned_data["page_content"]
            if page_title in entries1 :
                return render(request,"encyclopedia/newpage.html",{"newpageform": form,"error":'This entry already exists',"form": SearchForm()})
            else:
                util.save_entry(page_title,page_content)
                entries1.append(page_title)
                return render(request, "encyclopedia/entry.html", {
                    "content": markdown2.markdown(util.get_entry(page_title)), "form": SearchForm(),"title":page_title
                })

def edit(request,title):
    if request.method=="GET":
        content=util.get_entry(title)
        f = editform(initial={'content': content})
        return render(request,"encyclopedia/edit.html",{"editform": f,"form": SearchForm(),"title":title})
    else:
        form = editform(request.POST)
        if form.is_valid():
            form_content=form.cleaned_data["content"]
            util.save_entry(title,form_content)
            return render(request,"encyclopedia/entry.html",{"content":markdown2.markdown(util.get_entry(title)), "form": SearchForm(),"title":title})

def random_function(request):
    randomentry=random.choice(entries1)
    return render(request,"encyclopedia/entry.html",{"content":markdown2.markdown(util.get_entry(randomentry)), "form": SearchForm(),"title":randomentry})




