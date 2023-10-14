import django
import os
import sys

from collections import Counter

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from post.models import Post, Trend

def extract_hashtags(text, trends):
  for word in text.split():
    if word[0] == '#':
      trends.append(word[1:])

  return trends

for trend in Trend.objects.all():
  trend.delete()

posts = Post.objects.all()
trends = []

for post in posts:
  extract_hashtags(post.body, trends)

trends_counter = Counter(trends).most_common(10)

for trend in trends_counter:
  Trend.objects.create(hashtag=trend[0], occurrences=trend[1])

