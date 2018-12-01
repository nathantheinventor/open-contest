from code.util import register

def test(_, __, user, ___):
    return f"Hello, {user.username}"

register.web("/index", "any", test)

# from code.util.db import Contest
# from .static import generate
# from code.generator.lib.htmllib import *
# from code.generator.lib.page import *
# import time
# import logging
# from code.generator.pages.leaderboard import setContestStart
# from threading import Timer

# def displayFutureContest(contest: Contest):
#     Page.setTitle(contest.name)
#     generate("problems.html", Page(
#         h1("&nbsp;"),
#         h1("Contest Starts in", cls="center"),
#         h1(contest.start, cls="countdown jumbotron center")
#     ))

# def displayPastContest(contest: Contest):
#     Page.setTitle("OpenContest")
#     generate("problems.html", Page(
#         h1("&nbsp;"),
#         h1("Contest is Over", cls="jumbotron center")
#     ))

# def displayCurrentContest(contest: Contest):
#     setContestStart(contest.start // 1000)
#     logging.info(contest.start)
#     Page.setTitle(contest.name)
#     probCards = []
#     for prob in contest.problems:
#         probCards.append(Card(
#             prob.title,
#             prob.description,
#             f"/static/problems/{prob.id}.html"
#         ))
#     generate("problems.html", Page(
#         h2("Problems", cls="page-title"),
#         *probCards
#     ))

# contests = []
# def manageContest(contest: Contest):
#     logging.info(f"Contest Changed: {contest.name}")
#     global contests
#     contests.append(contest)
#     contests = sorted(contests, key=lambda contest: contest.start)

#     # Figure out what contests are around the current time
#     curContest = None
#     for contest in contests:
#         if contest.start <= time.time() * 1000 <= contest.end:
#             curContest = contest
#             break
#     prevContests = [contest for contest in contests if contest.end < time.time() * 1000]
#     nextContests = [contest for contest in contests if time.time() * 1000 < contest.start]

#     # Figure out which contest to display
#     if curContest == None:
#         if len(nextContests) > 0:
#             displayFutureContest(nextContests[0])
#             t = Timer(nextContests[0].start // 1000 - time.time() - 1, manageContest, [nextContests[0]])
#             t.start()
#         elif len(prevContests) > 0:
#             displayPastContest(prevContests[-1])
#     else:
#         displayCurrentContest(curContest)

# def generateContests():
#     Contest.forEach(manageContest)
#     Contest.onSave(manageContest)
