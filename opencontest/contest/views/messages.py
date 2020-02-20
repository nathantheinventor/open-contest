import time

from django.http import JsonResponse

from contest.auth import logged_in_required
from contest.models.message import Message
from contest.models.user import User
from contest.pages.lib.htmllib import html_encode


@logged_in_required
def getMessages(request):
    timestamp = float(request.POST["timestamp"])
    user = User.get(request.COOKIES['user'])
    newTime = time.time() * 1000
    messages = Message.messagesSince(timestamp)
    applicable = [message.toJSON() for message in messages
                  if (message.toUser and message.toUser.id == user.id)
                  or message.isGeneral
                  or (message.isAdmin and user.isAdmin())
                  or message.fromUser.id == user.id]
    applicable = sorted(applicable, key=lambda msg: msg["timestamp"], reverse=True)
    return JsonResponse({
        "messages": applicable,
        "timestamp": newTime
    })


@logged_in_required
def sendMessage(request):
    message = Message()
    user = User.get(request.COOKIES['user'])
    message.fromUser = user
    message.message = html_encode(request.POST["message"])
    message.timestamp = time.time() * 1000
    if user.isAdmin():
        message.toUser = User.get(request.POST["to"])
        message.isGeneral = request.POST["to"] == "general"
        message.replyTo = request.POST.get("replyTo")
    else:
        message.isAdmin = True
    message.save()
    return JsonResponse("ok", safe=False)
