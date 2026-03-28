from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Blog, Like, Comment
from user.models import User


def get_current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        return User.objects.filter(id=user_id).first()
    return None


def blog_create(request):
    user_obj = get_current_user(request)
    if not user_obj:
        return redirect('user:login')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        cover_image = request.FILES.get('cover_image')
        category = request.POST.get('category')
        status = request.POST.get('status', 'published')
        tags = request.POST.get('tags', '')

        Blog.objects.create(
            title=title,
            content=content,
            img=cover_image,
            category=category,
            status=status,
            tags=tags,
            created_by=user_obj,
        )
        return redirect('user:profile')
    return render(request, 'blog/create_blog.html', {'user': user_obj})


def blog_list(request):
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    tab = request.GET.get('tab', 'recommended')
    
    user_obj = get_current_user(request)
    
    blogs = Blog.objects.filter(status='published')
    
    if search_query:
        blogs = blogs.filter(title__icontains=search_query)
    
    if category:
        blogs = blogs.filter(category=category)
    
    if tab == 'latest':
        blogs = blogs.order_by('-created_at')
    elif tab == 'popular':
        blogs = blogs.order_by('-views', '-created_at')
    else:
        blogs = blogs.order_by('-created_at')
    
    for blog in blogs:
        if blog.created_by:
            blog.display_author = blog.created_by.name or 'Anonymous'
        else:
            blog.display_author = 'Anonymous'
    
    categories = Blog.objects.values_list('category', flat=True).distinct()
    
    return render(request, 'blog/home.html', {
        'blogs': blogs, 
        'search_query': search_query,
        'selected_category': category,
        'current_tab': tab,
        'categories': categories,
        'logged_in_user': user_obj
    })


def blog_delete(request, blog_id):
    user_obj = get_current_user(request)
    if not user_obj:
        return redirect('user:login')
    
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.created_by_id != user_obj.id:
        return redirect('blog:blog_list')
    
    blog.delete()
    return redirect('user:profile')


def blog_update(request, blog_id):
    user_obj = get_current_user(request)
    if not user_obj:
        return redirect('user:login')
    
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.created_by_id != user_obj.id:
        return redirect('blog:blog_list')
    
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        cover_image = request.FILES.get('cover_image')
        if cover_image:
            blog.img = cover_image
        blog.category = request.POST.get('category')
        blog.status = request.POST.get('status', 'published')
        blog.tags = request.POST.get('tags', '')
        blog.save()
        return redirect('user:profile')
    return render(request, 'blog/update_blog.html', {'blog': blog, 'user': user_obj})


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.views = (blog.views or 0) + 1
    blog.save()
    
    if blog.created_by:
        blog.display_author = blog.created_by.name or 'Anonymous'
        blog.author_profile_pic = blog.created_by.profile_pic.url if blog.created_by.profile_pic else None
    else:
        blog.display_author = 'Anonymous'
        blog.author_profile_pic = None
    
    user_obj = get_current_user(request)
    
    user_liked = False
    if user_obj:
        user_liked = Like.objects.filter(blog=blog, user=user_obj).exists()
    
    comments = blog.comments.select_related('user').order_by('-created_at')
    
    return render(request, 'blog/blog_detail.html', {
        'blog': blog, 
        'logged_in_user': user_obj,
        'user_liked': user_liked,
        'comments': comments
    })


def toggle_like(request, blog_id):
    user_obj = get_current_user(request)
    if not user_obj:
        return JsonResponse({'error': 'Login required'}, status=401)
    
    blog = get_object_or_404(Blog, id=blog_id)
    like, created = Like.objects.get_or_create(blog=blog, user=user_obj)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'like_count': blog.like_count
    })


def add_comment(request, blog_id):
    user_obj = get_current_user(request)
    if not user_obj:
        return JsonResponse({'error': 'Login required'}, status=401)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if not content:
            return JsonResponse({'error': 'Comment cannot be empty'}, status=400)
        
        blog = get_object_or_404(Blog, id=blog_id)
        comment = Comment.objects.create(blog=blog, user=user_obj, content=content)
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'user_name': user_obj.name,
                'created_at': comment.created_at.strftime('%b %d, %Y'),
            },
            'comment_count': blog.comment_count
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)