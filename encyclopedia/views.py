from django.shortcuts import render, redirect
import markdown2
import os
from django.conf import settings
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random

from . import util

class NavaTaskForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter Title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter markdown content here'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def TITLE(request, name):
    entry = util.get_entry(name)
    if entry == None:
        entry = """## Error: Information Not Available

        The requested information for the given title is currently unavailable in Markdown format.

        Please check if the title is correct or try again later."""

    entry = markdown2.markdown(entry)
    return render(request, "encyclopedia/entry.html",{
        "entry": entry,
        "TITLE": name
    })
    

def search(request):
    name = request.GET.get('q')
    entry = util.get_entry(name)
    if entry == None:
        ent_list = util.list_entries()
        new_ent_list = []
        for items in ent_list:
            if name.lower() in items.lower(): 
                new_ent_list.append(items)
   
        return render(request, "encyclopedia/search.html", {
        "entries": new_ent_list
        })
    else:
        entry = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html",{
        "entry": entry,
        "TITLE": name
        })

def create(request):
    """if request.method == "post":
        directory = "entries"  # Relative path from the base directory
        file_names = []
        dir = os.path.join(settings.BASE_DIR, directory)
        for file in os.listdir(dir):
            if os.path.isfile(os.path.join(directory, file)):
                file_name = os.path.splitext(file)[0]
                file_names.append(file_name.lower())

        title = request.POST.get('title')
        if title.lower() in file_names:
            entry = ## Error: Information Already exist

                    The requested information for the given title is already available

                    Please check if the title is correct or try again later.
            title = "ERROR" 
            return render(request, "encyclopedia/entry.html",{
            "entry": entry,
            "TITLE": title
            })
        
        title = request.POST.get('title')
        mark_down_cont = request.POST.get('content')
        with open(f"entries/{title}.md", "w") as file:
            file.write(mark_down_cont)
        return redirect("TITLE", title)

    else:
    """
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
        "form": NavaTaskForm()
        })
    else:
        form = NavaTaskForm(request.POST)
        if not(form.is_valid()):
            # If the form is invalid, re-render the page with existing information.
            return render(request, "tasks/create.html", {
                "form": form
            })
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        entry_list = util.list_entries()
        entry_list = [item.lower() for item in entry_list]
        if title.lower() in entry_list:
            entry = """## Error: Information Already exist

                    The requested information for the given title is already available

                    Please check if the title is correct or try again later."""
            entry = markdown2.markdown(entry)
            title = "ERROR" 
            return render(request, "encyclopedia/entry.html",{
            "entry": entry,
            "TITLE": title
            })
        else:
            path = f"entries/{title}.md"
            fileout = open(path, "a")
            fileout.write(content)
            fileout.close()
            return HttpResponseRedirect(reverse("encyclopedia:TITLE",  args=[title]))
        
def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        initial_data = {
        'title': title,
        'content': content,
        }
        form = NavaTaskForm(initial=initial_data)
        return render(request, "encyclopedia/edit.html",{
            "form": form
        })
    else:
        form = NavaTaskForm(request.POST)
        if not(form.is_valid()):
            # If the form is invalid, re-render the page with existing information.
            return render(request, "tasks/create.html", {
                "form": form
            })
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        path = f"entries/{title}.md"
        fileout = open(path, "w")
        fileout.write(content)
        fileout.close()
        return HttpResponseRedirect(reverse("encyclopedia:TITLE",  args=[title]))
    
def Random(request):
    list = util.list_entries()
    title = random.choice(list)
    return HttpResponseRedirect(reverse("encyclopedia:TITLE",  args=[title]))
