from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from user.models import User


@csrf_exempt
def register_view(request):
    if request.session.get('user_id'):
        return redirect('blog:blog_list')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([first_name, last_name, name, email, password]):
            return render(request, 'user/register.html', {'error': 'All fields are required'})

        if User.objects.filter(email=email).exists():
            return render(request, 'user/register.html', {'error': 'Email already exists'})
        
        if User.objects.filter(name=name).exists():
            return render(request, 'user/register.html', {'error': 'Username already exists'})
        
        if password == confirm_password:
            user = User(first_name=first_name, last_name=last_name, name=name, email=email, password=password)
            user.save()
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return redirect('blog:blog_list')
        else:
            return render(request, 'user/register.html', {'error': 'Passwords do not match'})
    return render(request, 'user/register.html')


@csrf_exempt
def login_view(request):
    if request.session.get('user_id'):
        return redirect('blog:blog_list')
        
    if request.method == "POST":
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')
        
        user = User.objects.filter(name=name, password=password).first()
        
        if user is not None:
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            request.session['user_email'] = user.email
            return redirect('blog:blog_list')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid credentials'})
    return render(request, 'user/login.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('user:login')

def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user:login')
    
    user_obj = User.objects.filter(id=user_id).first()
    if not user_obj:
        return redirect('user:login')
    
    blogs = Blog.objects.filter(created_by=user_obj).order_by('-created_at')
    blog_count = blogs.count()
    published_count = blogs.filter(status='published').count()
    
    from blog.models import Like
    total_likes = Like.objects.filter(blog__in=blogs).count()
    
    return render(request, 'user/profile.html', {
        'blogs': blogs, 
        'blog_count': blog_count,
        'published_count': published_count,
        'total_likes': total_likes,
        'user': user_obj
    })


def user_search(request):
    query = request.GET.get('q', '').strip()
    users = []
    current_user_id = request.session.get('user_id')
    
    if query:
        users = User.objects.filter(name__icontains=query).exclude(id=current_user_id)[:10]
    
    return render(request, 'user/search.html', {
        'query': query,
        'users': users,
        'logged_in_user': User.objects.filter(id=current_user_id).first() if current_user_id else None
    })


def view_user(request, user_id):
    from blog.models import Like
    viewed_user = get_object_or_404(User, id=user_id)
    current_user_id = request.session.get('user_id')
    logged_in_user = User.objects.filter(id=current_user_id).first() if current_user_id else None
    
    blogs = Blog.objects.filter(created_by=viewed_user, status='published').order_by('-created_at')
    blog_count = blogs.count()
    total_likes = Like.objects.filter(blog__in=blogs).count()
    
    return render(request, 'user/view_user.html', {
        'viewed_user': viewed_user,
        'blogs': blogs,
        'blog_count': blog_count,
        'total_likes': total_likes,
        'logged_in_user': logged_in_user
    })


def edit_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user:login')
    
    user_obj = User.objects.filter(id=user_id).first()
    if not user_obj:
        return redirect('user:login')
    
    if request.method == 'POST':
        user_obj.name = request.POST.get('name', '')
        user_obj.bio = request.POST.get('bio', '')
        user_obj.github = request.POST.get('github', '')
        user_obj.instagram = request.POST.get('instagram', '')
        user_obj.facebook = request.POST.get('facebook', '')
        user_obj.twitter = request.POST.get('twitter', '')
        user_obj.linkedin = request.POST.get('linkedin', '')
        user_obj.website = request.POST.get('website', '')
        
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
            user_obj.profile_pic = profile_pic
        
        user_obj.save()
        return redirect('user:profile')
    
    return render(request, 'user/edit_profile.html', {'user': user_obj})


from blog.models import Blog