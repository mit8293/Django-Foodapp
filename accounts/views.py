from django.shortcuts import render, redirect, HttpResponse
from .forms import RegistrationForm
from .models import Account, Blog, Comment
from django.contrib import messages, auth

# login req
from django.contrib.auth.decorators import login_required

# for user verification /sending mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # User Activation
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, 'Account Created. We have sent you verification email to your email address [test@test.com]. Please verify.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == "POST":
        email = request.POST["Email"]
        password = request.POST["Password"]
        print(email)
        print(password)

        user = auth.authenticate(email=email, password=password)
        print(user)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Login Credentials!')
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # check the token
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congrats! Your account is active.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    if request.user.is_authenticated:
        user_obj = request.user
        print(user_obj)
    my_filtered_blogs = Blog.objects.filter(user=user_obj)
    # comments = Comment.objects.filter(blog=my_filtered_blogs)
    print(my_filtered_blogs)
    context = {
        'user_obj': user_obj,
        'my_filtered_blogs': my_filtered_blogs,

    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def add_blog(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_obj = request.user
            print(user_obj)
            return render(request, 'accounts/add_blog.html', {'userdata': user_obj})

    else:
        if request.user.is_authenticated:
            user_obj = request.user

        Blog.objects.create(
            title=request.POST['title'],
            description=request.POST['des'],
            ingredients=request.POST['ingredients'],
            procedure=request.POST['procedure'],
            categories=request.POST['cate'],
            pic=request.FILES['foto'],
            # user ek foreign key field hai, isiliye obj dena hai
            user=user_obj
            # ye object jiska session chalu hai uska hai
        )
        messages.success(request, 'Congrats! Your Recipe has been uploaded.')
        return redirect('dashboard')


@login_required(login_url='login')
def edit_blog(request, bid):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_obj = request.user
            blog_obj = Blog.objects.get(id=bid)
            print(blog_obj)
            print(user_obj)
            return render(request, 'accounts/edit_blog.html', {'userdata': user_obj, 'blog': blog_obj})

    else:
        user_obj = request.user
        blog_obj = Blog.objects.get(id=bid)
        if blog_obj.user == user_obj:
            print("done")
            blog_obj.title = request.POST['title']
            blog_obj.description = request.POST['des']
            blog_obj.ingredients = request.POST['ingredients']
            blog_obj.procedure = request.POST['procedure']
            blog_obj.categories = request.POST['cate']
            blog_obj.save()
            messages.success(request, 'Your Recipe has been edited.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Bhag CHutya')
            return redirect('dashboard')


@login_required(login_url='login')
def delete_blog(request, bid):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_obj = request.user
            blog_obj = Blog.objects.get(id=bid)
            if blog_obj.user == user_obj:
                blog_obj.delete()
                messages.success(request, 'Your Recipe has been deleted.')
                return redirect('dashboard')


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST['Email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset Password email
            current_site = get_current_site(request)
            mail_subject = "Please reset your Password"
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, 'Password reset link has been sent to your email address.')
            return redirect('login')

        else:
            messages.error(request, 'Account does not exists')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password!')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == "POST":
        password = request.POST['Password']
        confirm_password = request.POST['confirm_Password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'New Password successfully created')
            return redirect('login')

        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')
