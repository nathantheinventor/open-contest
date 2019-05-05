from code.util.db import Submission, User, Contest, Problem
from code.generator.lib.htmllib import *
from code.generator.lib.page import *
import logging
from code.util import register
import time

all_languages = {
    "c": "C",
    "cpp": "C++",
    "cs": "C#",
    "java": "Java",
    "python2":"Python 2",
    "python3":"Python 3",
    "ruby": "Ruby",
    "vb":"Visual Basic"
}


def leaderboard(params, user):
    contest = Contest.getCurrent() or Contest.getPast()
    if not contest:
        return Page(
            h1("&nbsp;"),
            h1("No Contest Available", cls="center")
        )
    elif contest.scoreboardOff <= time.time() * 1000 and not user.isAdmin():
        return Page(
            h1("&nbsp;"),
            h1("Scoreboard is off.", cls="center")
        )

    start = contest.start
    end = contest.end

    
    subs = {}
    for sub in Submission.all():
        if start <= sub.timestamp <= end and not sub.user.isAdmin():
            subs[sub.user.id] = subs.get(sub.user.id) or []
            subs[sub.user.id].append(sub)            
    
    problemSummary = {}
    for prob in contest.problems:
        problemSummary[prob.id] = [0, 0]

    scores = []
    for userid in subs:
        usersubs = subs[userid]
        scor = score(usersubs, start, problemSummary)
        scores.append((
            User.get(userid).username,
            scor[0],
            scor[1],
            scor[2],
            len(usersubs)
        ))
    scores = sorted(scores, key=lambda score: score[1] * 1000000000 + score[2] * 10000000 - score[3], reverse=True)
    
    ranks = [i + 1 for i in range(len(scores))]
    for i in range(1, len(scores)):
        u1 = scores[i]
        u2 = scores[i - 1]
        if (u1[1], u1[2], u1[3]) == (u2[1], u2[2], u2[3]):
            ranks[i] = ranks[i - 1]
    
    scoresDisplay = []
    for (name, solved, samples, points, attempts), rank in zip(scores, ranks):
        scoresDisplay.append(h.tr(
            h.td(rank, cls="center"),
            h.td(name),
            h.td(attempts, cls="center"),
            h.td(solved, cls="center"),
            h.td(samples, cls="center"),
            h.td(points, cls="center")
        ))

    problemSummaryDisplay = []
    for problem in contest.problems:
        problemSummaryDisplay.append(h.tr(
            h.td(problem.title),
            h.td(problemSummary[problem.id][0], cls="center"),
            h.td(problemSummary[problem.id][1], cls="center")
        ))

    return Page(
        h2("Leaderboard", cls="page-title"),
        div(cls="actions", contents=[
            h.button("Detailed Contest Report", cls="button create-message",onclick="window.location.href='/contestreport'")
        ]),
        h.table(
            h.thead(
                h.tr(
                    h.th("Rank", cls="center"),
                    h.th("User"),
                    h.th("Attempts", cls="center"),
                    h.th("Problems Solved", cls="center"),
                    h.th("Sample Cases Solved", cls="center"),
                    h.th("Penalty Points", cls="center")
                )
            ),
            h.tbody(
                *scoresDisplay
            )
        ),
        h2("Problem Summary", cls="page-title"),
        h.table(
            h.thead(
                h.tr(
                    h.th("Problem", cls="center"),
                    h.th("Attempts", cls="center"),
                    h.th("Solved", cls="center"),
                )
            ),
            h.tbody(
                *problemSummaryDisplay
            )
        ),
        div(cls="align-right", contents=[
            h.br(),
            h.button("Correct Log", cls="button", onclick="window.location='/correctlog'")
        ] if user.isAdmin() else []
        )
    )

def contestreport(params, user):
    contest = Contest.getCurrent() or Contest.getPast()
    if not contest:
        return Page(
            h1("&nbsp;"),
            h1("No Contest Available", cls="center")
        )
    
    start = contest.start
    end = contest.end
    problemSummaryreport = []
    
    subs = {}
    for sub in Submission.all():
        if start <= sub.timestamp <= end and not sub.user.isAdmin():
            subs[sub.user.id] = subs.get(sub.user.id) or []
            subs[sub.user.id].append(sub)  
            
    
    if start <= time.time() <= end:
        reportcols = [h.th("Rank"),h.th("Contestant"),h.th("Contestant ID"),h.th("Correct"),h.th("Penalty"),]
    else:
        reportcols = [h.th("Rank"),h.th("Contestant ID"),h.th("Correct"),h.th("Penalty"),]
        

    problemSummary = {}
    problems = []
    problemNum = 0
    for prob in contest.problems:
        problemSummary[prob.id] = [0, 0]
        problemNum += 1
        problems.append(prob.id)
        problemSummaryreport.append({"id":prob.id,"title":prob.title,"attempts":0,"correct":0}) 
        reportcols.append(h.th(f"{problemNum}", cls="center"))

    scores = []
    for user in subs:
        usersubs = subs[user]
        scor = score(usersubs, start, problemSummary)
        scores.append((
            User.get(user).username,
            scor[0],
            scor[1],
            scor[2],
            len(usersubs),
            user
        ))
    
    scores = sorted(scores, key=lambda score: score[1] * 1000000000 + score[2] * 10000000 - score[3], reverse=True)
    ranks = [i + 1 for i in range(len(scores))]
    for i in range(1, len(scores)):
        u1 = scores[i]
        u2 = scores[i - 1]
        if (u1[1], u1[2], u1[3]) == (u2[1], u2[2], u2[3]):
            ranks[i] = ranks[i - 1]
    

    log = []
    for (name, solved, samples, points, attempts, userid), rank in zip(scores, ranks):
        log.append({"rank":rank,"name":name,"userid":userid, "solved":solved, "points":points})
    
    deatiledContestDisplay = []
    for person in log:
        outproblems = []
        submissions = sorted(subs[person["userid"]], key=lambda sub: sub.timestamp) 
        for p in problems:
            p_trys = 0
            earliest_time = 0
            for s in submissions:
                if p == s.problem.id:
                    p_trys += 1
                    if s.result == "ok":
                        earliest_time = s.timestamp
                        break

            if earliest_time: 
                outproblems.append(h.td(f"({p_trys}) {datetime.utcfromtimestamp((earliest_time - start) / 1000).strftime('%H:%M')}"))
                for prob in problemSummaryreport:
                    if prob['id'] == p:
                        prob["attempts"] += p_trys
                        prob["correct"] += 1
                        prob[s.language] = prob.get(s.language, 0) + 1
                        
            elif p_trys:      
                outproblems.append(h.td(f"({p_trys}) -- "))
                for prob in problemSummaryreport:
                    if prob['id'] == p:prob["attempts"] += p_trys
                
            else:
                outproblems.append(h.td(f""))
            
        deatiledContestDisplay.append(h.tr(
            h.td(person["rank"]),
            h.td(person["name"]),
            h.td(person["name"]) if start  <= time.time() <=  end else "",
            h.td(person["solved"]),
            h.td(person["points"]),
            *outproblems
        ))


    lang_col = [h.td("#"),h.td("Title")]
    for lan in all_languages:
        lang_col.append(h.td(all_languages[lan]))
    lang_col.append(h.td("Total Count"))
    problemSummaryDisplay =[]
    LanguageDisplay = []
    i = 0
    for prob in problemSummaryreport:

        i += 1
        problemSummaryDisplay.append(h.tr(
            h.td(i),
            h.td(prob["title"]),
            h.td(prob["attempts"]),
            h.td(prob["correct"]),
        ))

        langcount = []
        total = 0
        for lan in all_languages:
            if lan in prob:
                total += prob[lan]
                langcount.append(h.td(prob[lan]))
            else: langcount.append(h.td(""))

        LanguageDisplay.append(h.tr(
            h.td(i),
            h.td(prob["title"]),
            *langcount,
            h.td(total) if total > 0 else h.td("")
        ))

    return Page(
        h2("FINAL STANDINGS", cls="page-title"),
        h.table(
            h.thead(h.tr(*reportcols)),
            h.tbody(*deatiledContestDisplay)
        ),
        h2("Problem Summary", cls="page-title"),
        h.table(
            h.thead(
                h.tr(
                    h.td("#"),
                    h.td("Title"),
                    h.td("Attempts"),
                    h.td("Correct")
                )
            ),
            h.tbody(*problemSummaryDisplay)
        ),
        h2("Language Breakdown", cls="page-title"),
        h.table(
            h.thead(h.tr(*lang_col)
            ),h.tbody(*LanguageDisplay)
        )
    )

def score(submissions: list, contestStart, problemSummary) -> tuple:
    """ Given a list of submissions by a particular user, calculate that user's score.
        Calculates score in ACM format. """
    contest = Contest.getCurrent() or Contest.getPast()
    solvedProbs = 0
    sampleProbs = 0
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
        sampleSolved = False
        
        for sub in subs:
            for res in sub.results[:sub.problem.samples]:
                if res != "ok":
                    break
            else:
                sampleSolved = True
            if sub.result != "ok":
                # Unsuccessful submissions count for 20 penalty points
                # But only if the problem is eventually solved
                points += 20
            else:
                # The first successful submission adds a penalty point for each
                #     minute since the beginning of the contest
                # The timestamp is in millis
                points += (sub.timestamp - contestStart) // 60000
                solved = True
                break
        
        # Increment attempts
        problemSummary[sub.problem.id][0] += 1

        # A problem affects the score only if it was successfully solved
        if solved:
            solvedProbs += 1
            penPoints += points
            problemSummary[sub.problem.id][1] += 1
        elif sampleSolved and contest.tieBreaker:
            sampleProbs += 1
    
    # The user's score is dependent on the number of solved problems and the number of penalty points
    return solvedProbs, sampleProbs, int(penPoints)

register.web("/leaderboard", "loggedin", leaderboard)
register.web("/contestreport", "loggedin", contestreport)
