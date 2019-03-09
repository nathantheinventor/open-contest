from opencontest.models import Problem, Contest
from opencontest.views.general import render_page, no_contest, get_person
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def list_problems(req):
    contest = Contest.current()
    if contest is None:
        return no_contest(req)
    return render_page(req, "opencontest/problems.html", {"problems": contest.problem_set.all()})

@login_required
def view_problem(req, id: int):
    contest = Contest.current()
    problem = Problem.objects.get(id=id)
    person = get_person(req)
    if (contest is None or problem.contest != contest) and not person.is_admin:
        return no_contest(req)
    
    return render_page(req, "opencontest/problem.html", {"problem": problem})

@user_passes_test(lambda u: u.is_superuser)
def edit_problem(req, id: int):
    pass
