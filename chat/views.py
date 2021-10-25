from django.shortcuts import render

def index(request , username , group_name):
    return render(request, 'chat/index.html' , {'username': username , 'group_name': group_name})
