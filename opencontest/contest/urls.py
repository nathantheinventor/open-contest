from django.urls import path

from contest.pages.contests import listContests, editContest
from contest.pages.judge import judge, judge_submission, judge_submission_close
from contest.pages.leaderboard import leaderboard, contestreport
from contest.pages.messages import displayMessages
from contest.pages.problemDisplay import listProblems, viewProblem
from contest.pages.problemEdit import editProblem, newProblem, listProblemsAdmin
from contest.pages.static import setup, fake_privacy, privacy, faqs, about
from contest.pages.submissions import getSubmissions, contestant_submission
from contest.pages.users import getUsers
from contest.pages.correctlog import generateLogReport
from contest.views.contests import deleteContest, createContest
from contest.views.generic import login, root, logout
from contest.views.messages import getMessages, sendMessage
from contest.views.problems import deleteProblem, createProblem
from contest.views.submit import submit, changeResult, rejudge, download, rejudgeAll
from contest.views.users import createUser, deleteUser

app_name = 'contest'
urlpatterns = [
    path('login', login, name='login'),
    path('privacy', privacy, name='privacy'),
    path('privacy2', fake_privacy, name='fake_privacy'),
    path('faqs', faqs, name='faqs'),
    path('about', about, name='about'),
    path('correctlog', generateLogReport, name='generateLogReport'),

    # logged in required
    path('', root, name='root'),
    path('logout', logout, name='logout'),

    path('problems', listProblems, name='listProblems'),
    path('problems/<uuid:id>', viewProblem, name='viewProblem'),

    path('getMessages', getMessages, name='getMessages'),
    path('sendMessage', sendMessage, name='sendMessage'),
    path('messages/<uuid:id>', displayMessages, name='displayMessages'),
    path('messages/inbox', displayMessages, name='inbox'),
    path('messages/processed', displayMessages, name='processed'),
    path('messages/announcements', displayMessages, name='announcements'),

    path('submit', submit, name='submit'),
    path('submissions', getSubmissions, name='getSubmissions'),
    path('contestantSubmission/<uuid:id>', contestant_submission, name='contestant_submission'),

    path('leaderboard', leaderboard, name='leaderboard'),
    path('contestreport', contestreport, name='contestreport'),

    # admin
    path('setup', setup, name='setup'),

    path('contests', listContests, name='listContests'),
    path('contests/<uuid:id>', editContest, name='editContestAdmin'),
    path('editContest', createContest, name='saveNewContest'),
    path('contests/new', editContest, name='createNewContest'),
    path('deleteContest', deleteContest, name='deleteContest'),

    path('problems_mgmt', listProblemsAdmin, name='adminListProblems'),
    path('problems/new', newProblem, name='newProblem'),
    path('problems/<uuid:id>/edit', editProblem, name='editProblem'),
    path('editProblem', createProblem, name='anotherEditProblem'),
    path('deleteProblem', deleteProblem, name='deleteProblem'),

    path('users', getUsers, name='getUsers'),
    path('createUser', createUser, name='createUser'),
    path('deleteUser', deleteUser, name='deleteUser'),

    path('judgeSubmission/<str:id>', judge_submission, name='judge_submission'),
    path('judgeSubmission/<uuid:id>/<str:force>', judge_submission, name='judge_submission'),
    path('judgeSubmissionClose', judge_submission_close, name='judge_submission_close'),
    path('judge', judge, name='judge'),
    path('changeResult', changeResult, name='changeResult'),
    path('rejudge', rejudge, name='rejudge'),
    path('download', download, name='download'),
    path('rejudgeAll', rejudgeAll, name='rejudgeAll')
]
