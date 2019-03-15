from code.generator.lib.htmllib import *
from code.generator.lib.page import *
from code.util.db import Message, User
from code.util import register

class MessageCard(UIElement):
    def __init__(self, msg: Message, user):
        if not user.isAdmin() or msg.fromUser.id == user.id:
            self.html = Card(
                f"Message from {msg.fromUser.username} at <span class='time-format'>{msg.timestamp}</span>",
                msg.message
            )
        else:
            self.html = Card(
                f"Message from {msg.fromUser.username} at <span class='time-format'>{msg.timestamp}</span>",
                msg.message,
                reply=f"reply('{msg.fromUser.id}')"
            )

def getMessages(params, user):
    messages = []
    Message.forEach(lambda msg: messages.append(msg) if ((msg.toUser and msg.toUser.id == user.id) or msg.fromUser.id == user.id or msg.isGeneral or (msg.isAdmin and user.isAdmin())) else None)
    messages = [*map(lambda msg: MessageCard(msg, user), sorted(messages, key=lambda msg: -msg.timestamp))]

    adminDetails = []
    if user.isAdmin():
        userOptions = [*map(lambda usr: h.option(usr.username, value=usr.id), User.all())]
        adminDetails = [
            h.h5("To"),
            h.select(cls="form-control recipient", contents=[
                h.option("general"),
                *userOptions
            ]),
            h.h5("Message")
        ]

    return Page(
        h2("Messages", cls="page-title"),
        div(cls="actions", contents=[
            h.button("+ Send Message", cls="button create-message", onclick="createMessage()")
        ]),
        Modal(
            "Send Message",
            div(
                *adminDetails,
                h.textarea(cls="message col-12")
            ),
            div(
                h.button("Cancel", **{"type":"button", "class": "button button-white", "data-dismiss": "modal"}),
                h.button("Send", **{"type":"button", "class": "button", "onclick": "sendMessage()"})
            )
        ),
        div(cls="message-cards", contents=messages),
    )

register.web("/messages/([a-z]+)", "loggedin", getMessages)