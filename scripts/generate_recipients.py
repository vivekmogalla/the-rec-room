import django
import os
import sys

from collections import Counter

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from post.models import Post, User



# extract users from post body
# def extract_users(text, users):
#   for word in text.split():
#     if word[0] == '@':
#       users.append(word[1:])

#   return users

# extract users and create post + user obj
def extract_users(post, recipients):
  users = []
  for word in post.body.split():
    if word[0] == '@':
      users.append(word[1:])
  
  if users:
    post_obj = { 'id': post.id, 'user': post.created_by, 'recipient': users }
    recipients.append(post_obj)

  return recipients

# don't need this, don't want to delete users
# for trend in Trend.objects.all():
#   trend.delete()

# get all usernames
for user in User.objects.all():
  print(user.username)

posts = Post.objects.all()
# users = []
recipients = []

# old fn call: extract user only
# for post in posts:
#   extract_users(post.body, users)

# new fn call: create post + user obj
for post in posts:
  extract_users(post, recipients)

# might want this for most-tagged recipients in total or per logged-in user
# users_counter = Counter(recipients).most_common(10)

print(recipients)

# for user in users_counter:
#   print(user)
  # User.objects.create(hashtag=trend[0], occurrences=trend[1])

