from django.shortcuts import render
from models import User
from django.http import JsonResponse

# Create your views here.
def user_list(request):
    users = User.objects.all().values()
    users_list = list(users)
    return JsonResponse(users_list, safe = False)
