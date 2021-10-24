from django.shortcuts import render

def index(request , username):
    return render(request, 'chat/index.html' , {'username': username})
