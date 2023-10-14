from django.forms import ModelForm
from django import forms

from .models import Post, Report
from account.models import User

from django.db.models import Q

class PostForm(ModelForm):
  class Meta:
    model = Post
    fields = ('body', 'title', 'media_type', 'recipients', 'genres', 'link',)

class ReportForm(ModelForm):
  class Meta:
    model = Report
    fields = ('type_of_report', 'body',)