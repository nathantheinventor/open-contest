from code.generator.lib.htmllib import *
from code.generator.lib.page import *
from code.util.db import Message, User
from code.util import register

class MessageCard(UIElement):
    def __init__(self, msglist, user):
        msg = msglist[0]
        if not user.isAdmin() or msg.fromUser.id == user.id:
            self.html = Card(
                f"Message from {msg.fromUser.username} at <span class='time-format' data_timestamp='{msg.timestamp}'>{msg.timestamp}</span>",
                msg.message
            )
        else:
            body = msg.message
            print('*** msglist = ', msglist)
            for reply in msglist[1:]:
                body += f"""\n<br><br>Reply from {reply.fromUser.username} at 
                    <span class='time-format' data_timestamp='{reply.timestamp}'>{reply.timestamp}</span>:<br>
                    {reply.message}"""
            self.html = Card(
                f"Message from judge at <span class='time-format' data_timestamp='{msg.timestamp}'>{msg.timestamp}</span>",
                body,
                reply=f"reply('{msg.fromUser.id}', '{msg.id}')"
            )

INBOX, PROCESSED, ANNOUNCEMENT = 'inbox', 'processed', 'announcements'

def getMessages(params, user):
    view = params[0]

    messages = []
    if view == INBOX:
        if user.isAdmin():
            inbox = {}
            Message.forEach(lambda msg: inbox.update({msg.id: msg}) if msg.isAdmin else None)

            # Remove from inbox messages that have been responded to
            Message.forEach(lambda msg: inbox.pop(msg.replyTo) if msg.replyTo in inbox else None)
            messages = list(inbox.values())
        else:
            Message.forEach(lambda msg: messages.append(msg) if (msg.toUser and msg.toUser.id == user.id or msg.fromUser == user or msg.isGeneral)  else None)

    elif view == PROCESSED:
        def addReply(msg):
            if msg.replyTo in replies:
                replies[msg.replyTo].append(msg)
            else:
                replies[msg.replyTo] = [msg]

        # Find replies
        replies = {}
        Message.forEach(lambda msg: addReply(msg) if msg.replyTo else None)

        messages = [[Message.get(id)] + replies[id] for id in replies.keys()]
    elif view == ANNOUNCEMENT:
        Message.forEach(lambda msg: messages.append(msg) if msg.isGeneral else None)

    if len(messages) > 0 and not isinstance(messages[0], list):
        messages = [[msg] for msg in messages]

    messages = [*map(lambda msglist: MessageCard(msglist, user), sorted(messages, key=lambda msglist: -msglist[0].timestamp))]

    adminDetails = []
    if user.isAdmin():
        userOptions = [*map(lambda usr: h.option(usr.username, value=usr.id), User.all())]
        adminDetails = [
            h.h5("To"),
            h.select(cls="form-control recipient", contents=[
                h.option("general"),
                *userOptions
            ]),
            h.input(type="hidden", id="replyTo"),
            h.h5("Message")
        ]

    if user.isAdmin():
        filter = div(
            a(href='inbox', contents="Inbox "),
            a(href='processed', contents="Handled "),
            a(href='announcements', contents="Announcements"),
        )
    else:
        filter = div()

    return Page(
        h2("Messages", cls="page-title"),
        div(cls="actions", contents=[
            h.button("+ Send Message", cls="button create-message", onclick="createMessage()")
        ]),
        filter,
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