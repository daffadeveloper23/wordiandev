from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import *
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token
from .models import *
# Create your views here.

# Basic functionality cluster
def index(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        published_content = Article.objects.filter(is_draft=False)
        return render(request, 'beranda.html', {
            'user_profile': user_profile,
            'published_content': published_content
        })
    else:
        return render(request, 'index.html')


@login_required(login_url='index')
def setting(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            first_name = request.POST['first']
            last_name = request.POST['last']
            
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.save()
        else:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            first_name = request.POST['first']
            last_name = request.POST['last']
            
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.save()
        
        return redirect('index')
    
    else:
        return render(request, 'init-setting.html', {
            'user_profile': user_profile
        })
        
    

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth-date')
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Try another username')
                return redirect('index')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('index')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )
                
                user.save()
                
                auth.login(request, auth.authenticate(username=username, password=password))
                
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(
                    user=user_model, 
                    id_user=user_model.id, 
                    email=email,
                    gender=gender,
                    birth_date=birth_date)
                new_profile.save()
                
                return redirect('setting')
  
def signin(request):
    if request.method == "POST":
        username = request.POST['signin-username']
        password = request.POST['signin-password']
        
        user = authenticate(username=username, password=password)
        
        if user != None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Credential invalid")
            return redirect('index')

@login_required(login_url='index')
def signout(request):
    auth.logout(request)
    return redirect('index')


# Write and edit cluster
@login_required(login_url='index')
def write_article(request):
    current_profile = Profile.objects.get(user=request.user)
    return render(request, 'writing-page.html', {
        "profile": current_profile
    })

@login_required(login_url='index')
def publish_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        subtitle = request.POST.get('subtitle')
        cover_image = request.FILES.get('cover-image')
        content = request.POST.get('article-content')
        author_profile = Profile.objects.get(user=request.user)
        
        if title != None and category != None and subtitle != None and cover_image != None and content != None:
            article = Article(
                title=title,
                subtitle=subtitle,
                cover_image=cover_image,
                content=content,
                author=request.user,
                is_draft=False,
                author_profile=author_profile,
                category=category
            )
            
            article.save()
            messages.info(request, 'Article saved and published')
        else:
            messages.info(request, "Failed to publish article. Please fill all inputs")
        return redirect('index')

@login_required(login_url='index')       
def save_draft(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        subtitle = request.POST.get('subtitle')
        cover_image = request.FILES.get('cover-image')
        content = request.POST.get('article-content')
        author_profile = Profile.objects.get(user=request.user)
        
        if title != None and category != None and subtitle != None and cover_image != None and content != None:
            article = Article(
                title=title,
                subtitle=subtitle,
                cover_image=cover_image,
                content=content,
                author=request.user,
                is_draft=True,
                author_profile=author_profile,
                category=category
            )
            
            article.save()
            messages.info(request, 'Success saved as draft')
        else:
            messages.info(request, "Failed to save as draft. Please fill all inputs")
        return redirect('index')

@login_required(login_url='index')    
def read_article(request, id):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    current_article = Article.objects.get(id=id)
    all_comments = Comment.objects.filter(commented_article=current_article)
    comment_count = len(all_comments)
    all_likes = LikeArticle.objects.filter(article_id=current_article.id)
    like_count = len(all_likes)
    
    user_like = LikeArticle.objects.filter(article_id=current_article.id, username=request.user.username)
    user_likes_it = False
    if len(user_like) > 0:
        user_likes_it = True
    else:
        user_likes_it = False
        
    user_following = FollowersCount.objects.filter(follower=request.user.username, user=current_article.author.username)
    is_following = False
    if len(user_following) > 0:
        is_following = True
    else:
        is_following = False
        
    read_other_articles = Article.objects.exclude(id=id)[:4]
    
    return render(request, "read-article.html", {
        "article": current_article,
        "user": user_profile,
        "user_object": user_object,
        "comments": all_comments,
        "comment_count": comment_count,
        "like_count": like_count,
        "user_likes_it": user_likes_it,
        "is_following": is_following,
        "other_articles": read_other_articles
    })
    
# Access the library
@login_required(login_url='index')
def acccess_library(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    literatures = Literature.objects.all()
    return render(request, "library.html", {
        "user_profile": user_profile,
        "literatures": literatures
    })
    
# Read a book
@login_required(login_url='index')
def read_book(request, id):
    literature_id = id
    all_notes = Note.objects.all() # Get all notes
    literature_instance = Literature.objects.get(id=literature_id)
    literature_instance.access_frequency += 1
    literature_instance.save()
    return render(request, "read-book.html", {
        "literature": literature_instance,
        "all_notes": all_notes
    })
    
# Make new note
@login_required(login_url='index')
def make_note(request):
    if request.method == "POST":
        
        title = request.POST["note-title"]
        content = request.POST["note-content"]
        literature_id = request.POST["literature_id"]
        
        new_note = Note(title=title, note=content)
        new_note.save()
        
        return redirect(f"read_book/{literature_id}")
        
@login_required(login_url='index')  
def update_note(request):
    content = request.POST["note-content"]
    literature_id = request.POST["literature_id"]
    note_id = request.POST["noteID"]
    
    current_note = Note.objects.get(id=note_id)
    
    current_note.note = content
    current_note.save()
    
    return redirect(f"read_book/{literature_id}")

# Post comment
@login_required(login_url='index')
def post_comment(request):
    if request.method == "POST":
        article_id = request.POST["article_id"]
        article_object = Article.objects.get(id=article_id)
        username = request.POST["username"]
        user_object = User.objects.get(username=username)
        commentator_profile = Profile.objects.get(user=user_object)
        comment = request.POST["comment"]
        
        new_comment = Comment(
            commentator=user_object,
            commented_article=article_object,
            comment=comment,
            commentator_profile=commentator_profile
        )
        
        new_comment.save()
        
        return redirect(f"read_article/{article_id}")
    
# View profile
@login_required(login_url='index')
def view_profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_article = Article.objects.filter(author=user_object, is_draft=False)
    user_article_count = len(user_article)
    
    if FollowersCount.objects.filter(follower=request.user.username, user=user_object.username).first():
        active_following = True
    else:
        active_following = False
        
    my_follower = FollowersCount.objects.filter(user=user_object.username)
    follower_count = len(my_follower)
    
    my_following = FollowersCount.objects.filter(follower=user_object.username)
    following_count = len(my_following)
    
    current_user_object = request.user
    current_user_profile = Profile.objects.get(user=current_user_object)
    return render(request, "profile.html", {
        "user_object": user_object,
        "user_profile": user_profile,
        "user_article": user_article,
        "user_article_count": user_article_count,
        "current_user_profile": current_user_profile,
        "active_following": active_following,
        "follower_count": follower_count,
        "following_count": following_count
    })
    
# View draft list
@login_required(login_url='index')
def draft_list(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    
    article_draft = Article.objects.filter(author=user_object, is_draft=True)
    article_draft_count = len(article_draft)
    
    return render(request, "draft-list.html", {
        "user_object": user_object,
        "user_profile": user_profile,
        "article_draft": article_draft,
        "article_draft_count": article_draft_count
    })
    
    
    
# Follow account
@login_required(login_url='index')
def follow(request):
    if request.method == "POST":
        follower = request.POST["follower"]
        user = request.POST["user"]
        
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect(f"/profile/{user}")
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect(f"/profile/{user}")
    else:
        return redirect('/')
    
@login_required(login_url='index')
def follow_from_article(request):
    if request.method == "POST":
        follower = request.POST["follower"]
        user = request.POST["user"]
        article_id = request.POST["article_id"]
        
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect(f"/read_article/{article_id}")
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect(f"/read_article/{article_id}")
    else:
        return redirect('/')
    
# Edit article
@login_required(login_url='index')
def edit_article(request, pk):
    current_article = Article.objects.get(id=pk)
    current_profile = Profile.objects.get(user=request.user)
    
    return render(request, "edit-article.html", {
        "current_article": current_article,
        "profile": current_profile
    })
    
@login_required(login_url='index')
def publish_draft(request):
    if request.method == "POST":
        current_article_id = request.POST["article-id"]
        current_article = Article.objects.get(id=current_article_id)
        
        if request.FILES.get('image') != None:
            title = request.POST.get('title')
            category = request.POST.get('category')
            subtitle = request.POST.get('subtitle')
            cover_image = request.FILES.get('cover-image')
            content = request.POST.get('article-content')
            
            if title != None and category != None and subtitle != None and content != None:
                current_article.title = title
                current_article.category = category
                current_article.subtitle = subtitle
                current_article.cover_image = cover_image
                current_article.content = content
                current_article.is_draft = False
                
                current_article.save()
            else:
                messages.info(request, "Failed to publish article. Please fill all inputs")
                return redirect('/')
        else:
            title = request.POST.get('title')
            category = request.POST.get('category')
            subtitle = request.POST.get('subtitle')
            content = request.POST.get('article-content')
            
            if title != "" and category != None and subtitle != "" and content != "":
                current_article.title = title
                current_article.category = category
                current_article.subtitle = subtitle
                current_article.content = content
                current_article.is_draft = False
                
                current_article.save()
            else:
                messages.info(request, "Failed to publish article. Please fill all inputs")
                return redirect('/')
        
        return redirect(f"profile/{request.user.username}")

@login_required(login_url='index')
def update_draft(request):
    if request.method == "POST":
        current_article_id = request.POST["article-id"]
        current_article = Article.objects.get(id=current_article_id)
        
        if request.FILES.get('image') != None:
            title = request.POST.get('title')
            category = request.POST.get('category')
            subtitle = request.POST.get('subtitle')
            cover_image = request.FILES.get('cover-image')
            content = request.POST.get('article-content')
            
            current_article.title = title
            current_article.category = category
            current_article.subtitle = subtitle
            current_article.cover_image = cover_image
            current_article.content = content
            current_article.is_draft = True
            
            current_article.save()
        else:
            title = request.POST.get('title')
            category = request.POST.get('category')
            subtitle = request.POST.get('subtitle')
            content = request.POST.get('article-content')
            
            current_article.title = title
            current_article.category = category
            current_article.subtitle = subtitle
            current_article.content = content
            current_article.is_draft = True
            
            current_article.save()
        
        return redirect(f"profile/{request.user.username}")
    
# Remove article
@login_required(login_url='index')
def remove_article(request, pk):
    current_article = Article.objects.get(id=pk)
    current_article.delete()
    
    return redirect("/profile/" + request.user.username)

# My Setting
@login_required(login_url='index')
def my_setting(request, pk):
    user_object = User.objects.get(username=pk)
    profile_object = Profile.objects.get(user=user_object)
    
    if request.user == user_object:
        return render(request, "my-setting.html", {
            "profile_object": profile_object,
            "user_object": user_object
        })
    else:
        return redirect('/')
    
# Edit setting
@login_required(login_url='index')
def edit_setting(request, pk):
    user_object = User.objects.get(username=pk)
    profile_object = Profile.objects.get(user=user_object)
    
    if request.user == user_object:
        return render(request, "edit-setting.html", {
            "user_profile": profile_object,
            "user_object": user_object
        })
    else:
        return redirect('/')
    
# Update setting
@login_required(login_url='index')
def update_setting(request):
    username = request.POST["username"]
    init_email = request.POST["initiated-email"]
    email = request.POST['email']
    
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)
    
    requested_email = request.POST["email"]
    if request.method == "POST":
        
        if init_email != email and User.objects.filter(email=requested_email).exists():
            messages.success(request, "Email already exist, update failed")
            return redirect(f"my-setting/{username}")
        else:
            if request.FILES.get('image') != None:
                image = request.FILES.get('image')
                bio = request.POST['bio']
                location = request.POST['location']
                first_name = request.POST['first']
                last_name = request.POST['last']
                
                
                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.first_name = first_name
                user_profile.last_name = last_name
                user_profile.email = email
                
                user_object.email = email
                
                user_profile.save()
                user_object.save()
            else:
                
                bio = request.POST['bio']
                location = request.POST['location']
                first_name = request.POST['first']
                last_name = request.POST['last']
                
                user_profile.bio = bio
                user_profile.location = location
                user_profile.first_name = first_name
                user_profile.last_name = last_name
                user_profile.email = email
                
                user_object.email = email
                
                user_profile.save()
                user_object.save()
        
    return redirect(f"my-setting/{username}")

# Verify email
@login_required(login_url='index')
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user_profile = Profile.objects.get(user=user)
    except:
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user_profile.verified_email = True
        
        user.save()
        user_profile.save()
        
        messages.success(request, "Email verification success")
    else:
        messages.error(request, "Email verification failed")
    
    return redirect('/')

@login_required(login_url='index')
def activate_email(request, user, to_email):
    user_object = User.objects.get(username=user)
    mail_subject = "Verify your email"
    
    message = render_to_string("template_activate_email.html", {
        'user': user_object.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user_object.pk)),
        'token': account_activation_token.make_token(user_object),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Dear, {user_object} please check {to_email}")
    else:
        messages.error(request, f"Problem sending email to {to_email}")

@login_required(login_url='index') 
def verify_email(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        activate_email(request, username, email)
        
        return redirect(f"my-setting/{username}")
    
# Like post
@login_required(login_url='index')
def like_article(request):
    if request.method == "POST":
        article_id = request.POST["article_id"]
        username = request.user.username
        
        article = Article.objects.get(id=article_id)
        like_filter = LikeArticle.objects.filter(article_id=article_id, username=username).first()
        
        if like_filter == None:
            new_like = LikeArticle.objects.create(article_id=article_id, username=username)
            new_like.save()
            article.no_of_like = article.no_of_like + 1
            article.save()
            
            return redirect(f"read_article/{article_id}")
        else:
            like_filter.delete()
            article.no_of_like = article.no_of_like - 1
            article.save()
            
            return redirect(f"read_article/{article_id}")
        
# Search article
@login_required(login_url='index')
def search(request):
    if request.method == "POST":
        search_text = request.POST["search-title"]
        all_articles = Article.objects.all()
        suggested_result = []
        
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        
        for article in all_articles:
            if search_text.lower() in article.title.lower():
                suggested_result.append(article)
                
        suggested_result_count = len(suggested_result)
        
        return render(request, "search-result.html", {
            "user_profile": user_profile,
            "suggested_result": suggested_result,
            "suggested_result_count": suggested_result_count
        })
        