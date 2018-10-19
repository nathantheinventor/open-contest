from .htmllib import *
from .page import Card
from ..db import getKey

from datetime import datetime, tzinfo, timezone

class SubmissionDisplay(UIElement):
    def __init__(self, submission):
        subTime = submission["timestamp"]
        prob = submission["problem"]
        probName = getKey("/problems/{}/problem.json".format(prob))["title"]
        cls = "red" if submission["result"] != "ok" else ""
        self.html = Card("Submission to {} at <span class='time-format'>{}</span>".format(probName, subTime), [
            h.strong("Language: <span class='language-format'>{}</span>".format(submission["language"])),
            h.br(),
            h.strong("Result: <span class='result-format'>{}</span>".format(submission["result"])),
            h.br(),
            h.br(),
            h.strong("Code:"),
            h.code(submission["code"].replace("\n", "<br/>").replace(" ", "&nbsp;"))
        ], cls=cls)
