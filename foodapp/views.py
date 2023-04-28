from django.shortcuts import render, HttpResponse, redirect
from accounts.models import Account, Blog, Comment
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def recipes(request):
    filtered_blogs = Blog.objects.all()
    paginator = Paginator(filtered_blogs, 2)
    page = request.GET.get('page')
    paged_blogs = paginator.get_page(page)
    latest_blogs = Blog.objects.all().order_by('-time')[:3]

    context = {
        'blogs': paged_blogs,
        'latest_blogs': latest_blogs,
    }
    return render(request, 'store/store.html', context)


def veg(request):
    # all_blogs = Blog.objects.all()
    filtered_blogs = Blog.objects.filter(categories='veg')
    context = {
        'blogs': filtered_blogs,
    }
    return render(request, 'store/store.html', context)


def nonveg(request):
    # all_blogs = Blog.objects.all()
    filtered_blogs = Blog.objects.filter(categories='nonveg')
    context = {
        'blogs': filtered_blogs,
    }
    return render(request, 'store/store.html', context)


def healthy(request):
    # all_blogs = Blog.objects.all()
    filtered_blogs = Blog.objects.filter(categories='healthy')
    context = {
        'blogs': filtered_blogs,
    }
    return render(request, 'store/store.html', context)


@login_required(login_url='login')
def singleblog(request, pk):

    s_blog = Blog.objects.get(id=pk)
    filtered_comments = Comment.objects.filter(blog=s_blog)
    count = filtered_comments.count()
    # d_list = Donation.objects.filter(pay_to = s_blog)
    # d_amount = 0
    # for i in d_list:
    #     d_amount += i.amount
    return render(request, 'store/single_blog.html', {"blog": s_blog, 'all_comments': filtered_comments, 'count': count})


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            blogs = Blog.objects.order_by(
                '-time').filter(Q(description__icontains=keyword) | Q(title__icontains=keyword))
            blogs_count = blogs.count()
    context = {
        'blogs': blogs,
        'Product_count': blogs_count,
    }
    return render(request, 'store/store.html', context)


@login_required(login_url='login')
def add_comment(request, bid):
    try:
        if request.user.is_authenticated:
            user_obj = request.user
            print(user_obj)
        blog_obj = Blog.objects.get(id=bid)
        Comment.objects.create(
            message=request.POST['troll'],
            blog=blog_obj,
            user=user_obj
        )
        return redirect(f'/singleblog/{bid}')
    except Exception as e:
        print(e)
        return redirect('login')
