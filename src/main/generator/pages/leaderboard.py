from code.util.db import Submission, User
from .static import generate
from code.generator.lib.htmllib import *
from code.generator.lib.page import *

contestStart = 1500000000

submissions = {}
leaderboard = {}

def displayLeaderboard():
    scores = []
    for user in leaderboard:
        scores.append((
            User.get(user).username,
            leaderboard[user][0],
            leaderboard[user][1]
        ))
    scores = sorted(scores, key=lambda score: score[1] * 1000000000 - score[1], reverse=True)
    
    ranks = [i + 1 for i in range(len(scores))]
    for i in range(1, len(scores)):
        u1 = scores[i]
        u2 = scores[i - 1]
        if (u1[1], u1[2]) == (u2[1], u2[2]):
            ranks[i] = ranks[i - 1]
    
    scoresDisplay = []
    for (name, solved, points), rank in zip(scores, ranks):
        scoresDisplay.append(h.tr(
            h.td(name),
            h.td(solved, cls="center"),
            h.td(points, cls="center"),
            h.td(rank, cls="center")
        ))

    generate("leaderboard.html", Page(
        h2("Leaderboard", cls="page-title"),
        h.table(
            h.thead(
                h.tr(
                    h.th("User"),
                    h.th("Problems Solved", cls="center"),
                    h.th("Penalty Points", cls="center"),
                    h.th("Rank", cls="center")
                )
            ),
            h.tbody(
                *scoresDisplay
            )
        )
    ))

def score(submissions: list) -> tuple:
    """ Given a list of submissions by a particular user, calculate that user's score.
        Calculates score in ACM format. """
    
    solvedProbs = 0
    penPoints = 0

    # map from problems to list of submissions
    probs = {}

    # Put the submissions into the probs list
    for sub in submissions:
        probId = sub.problem.id
        if probId not in probs:
            probs[probId] = []
        probs[probId].append(sub)
    
    # For each problem, calculate how much it adds to the score
    for prob in probs:
        # Sort the submissions by time
        subs = sorted(probs[prob], key=lambda sub: sub.timestamp)
        # Penalty points for this problem
        points = 0
        solved = False
        
        for sub in subs:
            if sub.result != "ok":
                # Unsuccessful submissions count for 20 penalty points
                # But only if the problem is eventually solved
                points += 20
            else:
                # The first successful submission adds a penalty point for each
                #     minute since the beginning of the contest
                # The timestamp is in millis
                points += (sub.timestamp - contestStart) // 60
                solved = True
                break
        
        # A problem affects the score only if it was successfully solved
        if solved:
            solvedProbs += 1
            penPoints += points
    
    # The user's score is dependent on the number of solved problems and the number of penalty points
    return solvedProbs, penPoints

def addSubmission(sub: Submission):
    # Add submission to the list of submissions for this user
    user = sub.user.id
    if user not in submissions:
        submissions[user] = {sub}
    submissions[user].add(sub)

    # Sort the submissions from newest to oldest
    subs = sorted(submissions[user], key=lambda sub: sub.timestamp, reverse=True)
    leaderboard[user] = score(subs)
    displayLeaderboard()

def generateLeaderboard():
    Submission.forEach(addSubmission)
    Submission.onSave(addSubmission)
