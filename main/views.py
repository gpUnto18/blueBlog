from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import datetime, time
import pytz
import json

from django.contrib import messages

from django.conf import settings

import json
import urllib
import urllib.request

from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import Post, Me, Info, Link, Comment, GalleryImage, AdminLoginAttempts

#def error_404(request):
#        data = {}
#        return render(request,'blog/error_404.html', data)

#def error_500(request):
#        data = {}
#        return render(request,'blog/500.html', data)

def home(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    paginator = Paginator(posts, 15)
    page = request.GET.get('page')

    postsP = paginator.get_page(page)


    mes = Me.objects.all()
    infos = Info.objects.all()
    links = Link.objects.all()
    return render(request, 'blog/home.html', {'posts': posts , 'mes': mes, 'infos': infos, 'links': links, 'postsP': postsP})

def post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-published_date')
    return render(request, 'blog/post.html', {'post': post, 'comments': comments})

def search(request):
    input = request.GET['search-text']
    posts = Post.objects.filter(title__contains=input)
    return render(request, 'blog/search.html', {'posts': posts})

def comment(request, pk):

    #Begin reCAPTCHA validation
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req =  urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    #End reCAPTCHA validation

    post = get_object_or_404(Post, pk=pk)

    if result['success']:
        c = Comment(post=post, author="gp-18", title=request.POST.get('comment-title'), text=request.POST.get('comment-text'))
        c.save()
        # if invalid comment -> render post + errors (dict)

    return redirect('post', pk=post.pk)


def deleteComment(request, cPK, pPK):
    if request.user.is_authenticated:
        c = Comment.objects.get(pk=cPK)
        c.delete()
        return redirect('post', pk=pPK)
    else:
        return redirect('home')

def gallery(request):
    images = GalleryImage.objects.order_by('-created_date')
    imgs = []
    dict = {}
    n = 1

    for x in images:
        data = {}
        data['image'] = x.image
        data['id'] = n
        data['pk'] = x.pk
        imgs.append(data)

        dict[n] = x.pk

        n = n + 1

    imageDict = json.dumps(dict)

    return render(request, 'blog/gallery.html', {'images': imgs, 'imageDict': imageDict})

def documents(request):
    return render(request, 'blog/documents.html')

def admin(request):
    firstLogin = True
    maxAttempts = False
    numberOfGroups = AdminLoginAttempts.objects.count()
    utc = pytz.UTC
    loginGroup = AdminLoginAttempts.objects.get(group=1)

    if numberOfGroups == 0:
        loginAttemps = AdminLoginAttempts(group=1, attempts=0, lastTime=datetime.datetime.now())
        loginAttemps.save()
    else:
        lastTime = loginGroup.lastTime
        attempts = loginGroup.attempts
        now = utc.localize(datetime.datetime.now())
        seconds = int((now-lastTime).total_seconds())

        if seconds>300:
            loginGroup.lastTime = now
            loginGroup.attempts = 0
            loginGroup.save()
        elif attempts<3:
            loginGroup.attempts = attempts+1
            loginGroup.save()
        else:
            maxAttempts = True


    if request.method == 'POST':
        un = request.POST.get('login-name')
        pw = request.POST.get('login-pw')
        user = authenticate(request, username=un, password=pw)

        if user is not None:
            loginGroup.lastTime = now
            loginGroup.attempts = 0
            loginGroup.save()
            login(request, user)
        else:
            firstLogin = False

    me = Me.objects.all().first()
    return render(request, 'blog/admin.html', {'me': me, 'firstLogin': firstLogin, 'maxAttempts': maxAttempts, 'seconds': seconds})

def adminLogin(request):
    un = request.POST.get('login-name')
    pw = request.POST.get('login-pw')
    user = authenticate(request, username=un, password=pw)

    if user is not None:
        login(request, user)

    return redirect('admin')

def addPicture(request):
    pictures = request.FILES.getlist('gallery-pictures')
    for p in pictures:
        gi = GalleryImage(image=p, title=p.name)
        gi.save()
    return redirect('gallery')

def deletePicture(request, pk):
    if request.user.is_authenticated:
        i = GalleryImage.objects.get(pk=pk)
        i.delete()
        return redirect('gallery')
    else:
        return redirect('home')

def adminLogout(request):
    logout(request)
    return redirect('home')

def addPost(request):
    currentAuthor = request.user
    postTitle = request.POST.get('post-title')
    postText = request.POST.get('post-text')
    now = datetime.datetime.now()
    if request.FILES:
        picture = request.FILES['post-picture']
        post = Post(author=currentAuthor, published_date=now, title=postTitle, text=postText, image=picture)
    else:
        post = Post(author=currentAuthor, published_date=now, title=postTitle, text=postText)
    post.save()
    return redirect('home')

def deletePost(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('home')
    else:
        return redirect('home')

def editPost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/editpost.html', {'post': post})

def changeMe(request):
    me = Me.objects.all().first()
    meDescription = request.POST.get('me-description')
    if request.FILES:
        mePicture = request.FILES['me-picture']
        me.image = mePicture
    me.description = meDescription
    me.save()
    return redirect('home')

def applyPostChanges(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-published_date')
    postTitle = request.POST.get('post-title')
    postText = request.POST.get('post-text')
    post.title = postTitle
    post.text = postText
    if request.FILES:
        postImage = request.FILES['post-picture']
        post.image = postImage
    post.save()
    return render(request, 'blog/post.html', {'post': post, 'comments': comments})



