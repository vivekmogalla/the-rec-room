from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import requests

from .serializers import PostSerializer, LikeSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer, MediaTypeSerializer, GenreSerializer
from .models import Post, Like, Comment, Report, Trend, MediaType, Save
from .forms import PostForm

from account.models import User
from account.serializers import UserSerializer
from notification.utils import create_notification

# @api_view(['GET'])
def post_list(request):
    import pdb; pdb.set_trace()
    posts = Post.objects.all()
    trend = request.GET.get('trend', '')
    media_type_id = request.GET.get('mediaType', '')

    if trend:
        posts = posts.filter(body__icontains='#'+trend)
    elif media_type_id:
        media_type = MediaType.objects.get(pk=media_type_id)
        posts = media_type.posts.all()

    posts = posts[:16]

    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, id):
    post = Post.objects.get(pk=id)
    user = User.objects.get(pk=post.created_by_id)

    return JsonResponse({
        'post': PostDetailSerializer(post).data,
        'user': UserSerializer(user).data,
    })


# Figure out how to consolidate these two functions!!!!
# how do you pass a variable through a GET call??
@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)[:16]

    user_serializer = UserSerializer(user)
    posts_serializer = PostSerializer(posts, many=True)

    return JsonResponse({
        'user': user_serializer.data,
        'posts': posts_serializer.data
    }, safe=False)


@api_view(['GET'])
def post_list_profile_received(request, id):
    user = User.objects.get(pk=id)
    posts = user.received_recs.all()

    user_serializer = UserSerializer(user)
    posts_serializer = PostSerializer(posts, many=True)

    return JsonResponse({
        'user': user_serializer.data,
        'posts': posts_serializer.data
    }, safe=False)


@api_view(['GET'])
def post_list_profile_saved(request, id):
    user = User.objects.get(pk=id)
    saves = user.saved_recs.all()

    posts = []
    for save in saves:
        posts.append(save.post_set.first())

    user_serializer = UserSerializer(user)
    posts_serializer = PostSerializer(posts, many=True)

    return JsonResponse({
        'user': user_serializer.data,
        'posts': posts_serializer.data
    }, safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.data)
    recipients = request.data.get('recipients')

    link = request.data.get('link')
    link_response = {}

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        form.save_m2m()

        if link:
            print(link)
            link_request = requests.get(f'https://jsonlink.io/api/extract?url={link}')
            print(f'link request: {link_request}')
            link_status = link_request.status_code
            print(f'link status: {link_status}')
            link_data = link_request.json()
            print(f'link data to json: {link_data}')
            if link_status == 200:
                link_response['status'] = 200
                link_response['description'] = link_data['description']
                link_response['domain'] = link_data['domain']
                link_response['title'] = link_data['title']
                link_response['images'] = link_data['images']

            print(link_response)

        for recipient in recipients:
            notification = create_notification(request, 'post_tag', post_id=post.id, recipient_id=recipient)

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'error creating post'})


@api_view(['POST'])
def post_edit(request, id):
    post = Post.objects.get(pk=id)
    body = request.data.get('body')

    post.body = body
    post.save()

    return JsonResponse({'message': 'post edited'})


@api_view(['DELETE'])
def post_delete(request, id):
    post = Post.objects.get(pk=id)
    post.delete()

    return JsonResponse({'message': 'post deleted'})


@api_view(['POST'])
def post_report(request, id):
    post = Post.objects.get(pk=id)
    body = request.data.get('body')
    type_of_report = request.data.get('type_of_report')
    created_by = request.user
    
    report = Report.objects.create(
        body=body, 
        type_of_report=type_of_report, 
        created_by=created_by, 
        post=post
    )

    return JsonResponse({'message': 'post reported'})


@api_view(['GET', 'POST'])
def post_like(request, id):
    post = Post.objects.get(pk=id)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        message = 'like created'
        if not post.likes.filter(created_by=request.user):
            like = Like.objects.create(created_by=request.user)
        
            post.likes_count += 1
            post.likes.add(like)
            post.save()

            serializer = PostSerializer(post)

            notification = create_notification(request, 'post_like', post_id=post.id)

            return JsonResponse({
                'message': message,
                'post_like': serializer.data,
            }, safe=False)
        else:
            like = post.likes.get(created_by=request.user)

            post.likes_count -= 1
            post.likes.remove(like)
            post.save()
            like.delete()

            message = 'like removed'
            serializer = PostSerializer(post)

            return JsonResponse({
                'message': message,
                'post_like': serializer.data,
            }, safe=False)


@api_view(['GET', 'POST'])
def post_save(request, id):
    post = Post.objects.get(pk=id)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        message = 'post saved'
        if not post.saved_recs.filter(created_by=request.user):
            save = Save.objects.create(created_by=request.user)
        
            post.saves_count += 1
            post.saved_recs.add(save)
            post.save()

            serializer = PostSerializer(post)

            notification = create_notification(request, 'post_save', post_id=post.id)

            return JsonResponse({
                'message': message,
                'post_save': serializer.data,
            }, safe=False)
        else:
            save = post.saved_recs.get(created_by=request.user)

            post.saves_count -= 1
            post.saved_recs.remove(save)
            post.save()
            save.delete()

            message = 'post unsaved'
            serializer = PostSerializer(post)

            return JsonResponse({
                'message': message,
                'post_save': serializer.data,
            }, safe=False)


@api_view(['POST'])
def post_create_comment(request, id):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)
    post = Post.objects.get(pk=id)
    
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()

    notification = create_notification(request, 'post_comment', post_id=post.id)
    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)


@api_view(['DELETE'])
def post_delete_comment(request, id, pk):
    comment = Comment.objects.get(pk=pk)
    post = Post.objects.get(pk=id)

    post.comments.remove(comment)
    post.comments_count = post.comments_count - 1
    post.save()

    comment.delete()

    return JsonResponse({'message': 'comment deleted'})


@api_view(['POST'])
def post_report_comment(request, id):
    comment = Comment.objects.get(pk=id)
    body = request.data.get('body')
    type_of_report = request.data.get('type_of_report')
    created_by = request.user
    
    report = Report.objects.create(
        body=body, 
        type_of_report=type_of_report, 
        created_by=created_by, 
        comment=comment
    )

    return JsonResponse({'message': 'comment reported'})


@api_view(['GET'])
def get_trends(request):
    trends = Trend.objects.all()
    serializer = TrendSerializer(trends, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def get_media_types(request):
    types = MediaType.objects.exclude(name='Media')
    serializer = MediaTypeSerializer(types, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def get_genres(request):
    media_id = request.GET.get('mediaType',)
    media_type = MediaType.objects.get(pk=media_id)
    
    genres = media_type.genres
    serializer = GenreSerializer(genres, many=True)

    return JsonResponse(serializer.data, safe=False)
    