from .problems import generateProblems
from .submissions import generateSubmissions
from .leaderboard import generateLeaderboard

def generateDynamic():
    generateProblems()
    generateSubmissions()
    generateLeaderboard()