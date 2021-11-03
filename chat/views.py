from channels.layers import get_channel_layer
from django.shortcuts import render
from asgiref.sync import async_to_sync
from django.http import HttpResponse,HttpResponseServerError , HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt


def index(request , username , group_name):
    return render(request, 'chat/index.html' , {'username': username , 'group_name': group_name})

@csrf_exempt
def send_group_message(requset):
    try:
        if requset.method == "GET":
            return HttpResponseNotAllowed("Method Not Allowed .")
        sender = requset.POST.get("user_name" , None)
        group_name = requset.POST.get("group_name" , None)
        message = requset.POST.get("message" , None)

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"group_{group_name}",
            {
                'type': 'chat_group_message',
                'message': message,
                'sender' : sender,
            }
        )
        return HttpResponse("ok .")
    except:
        return HttpResponseServerError("Internal Server Error, We'll Check It Later")