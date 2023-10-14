from django.shortcuts import render
from django.http import HttpResponse

from .models import User

def activate_email(request):
  email = request.GET.get('email', '')
  id = request.GET.get('id', '')

  if email and id:
    user = User.objects.get(id=id, email=email)
    user.is_active = True
    user.save()

    return HttpResponse('Your account is now active! Please log in to continue setting up your profile.')

  else:
    return HttpResponse('Something went wrong...')
