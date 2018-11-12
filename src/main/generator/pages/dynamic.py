from .problems import generateProblems
from .submissions import generateSubmissions
from .leaderboard import generateLeaderboard
from .contest import generateContests

def generateDynamic():
    generateProblems()
    generateSubmissions()
    generateContests()
    generateLeaderboard()
