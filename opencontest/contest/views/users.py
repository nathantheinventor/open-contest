from django.http import JsonResponse

from contest.auth import generatePassword, admin_required
from contest.models.user import User


@admin_required
def createUser(request):
    newPassword = generatePassword()
    user = User(
        request.POST["username"],
        newPassword,
        request.POST["type"]
    )
    user.save()
    return JsonResponse(newPassword, safe=False)


@admin_required
def deleteUser(request):
    username = request.POST["username"]
    user = User.getByName(username)
    user.delete()
    return JsonResponse("ok", safe=False)
