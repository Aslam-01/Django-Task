from functools import wraps
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
# from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import jwt
from datetime import datetime, timedelta
# from django.contrib.auth.decorators import permission_required,login_required
from .models import User
from django.core.paginator import Paginator


def index(request):
    return render(request, 'app/basic.html')

def generate_access_token(user):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token

@csrf_exempt
def signup(request):
    choices = User.COURSE_CHOICES
    if request.method == 'POST':
        # print("*************","Post")
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        city = request.POST.get('city')
        course = request.POST.get('course', '')
        password = request.POST.get('password')
        user = User.objects.create_user(name=name, email=email, phone=phone, dob=dob, city=city, password=password,course=course)
        if user:
            return redirect('login')
        else:
            return HttpResponse('Failed to create user', status=400)
    # print("********************","Get")
    return render(request,'app/signup.html',{'choices':choices})

def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')
        if access_token:
            try:
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload['user_id']
                user = User.objects.get(id=user_id)
                request.user = user
                return view_func(request, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return HttpResponse('Session expired. Please login again.', status=401)
            except jwt.InvalidTokenError:
                return HttpResponse('Invalid token. Please login again.', status=401)
        else:
            return redirect('login')
    return wrapper

@custom_login_required
def add(request):
    choices = User.COURSE_CHOICES
    if request.method == "POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        dob=request.POST.get('dob','')
        # print("---------------------------->",dob)
        city=request.POST.get('city','')
        course=request.POST.get('course','')
        post=User(name=name,email=email,phone=phone,dob=dob,city=city,course=course)
        post.save()
    return render(request,'app/student.html',{'choices':choices})

@custom_login_required
def search(request):
    courses = User.objects.all()
    choices = User.COURSE_CHOICES
    if request.method == "POST":
        data=request.POST.get('course','')
        courses=User.objects.filter(course__icontains=data)
        return render(request,'app/dashboard.html',{'courses':courses})
    # courses=
    return render(request,'app/dashboard.html',{'courses':courses,'choices':choices})

@custom_login_required
def update(request):
    user=User.objects.all()
    alert = request.session.get('user',False)
    
    if request.method == "POST":
        data=request.POST.get('update','')
        userfinal=User.objects.filter(id=data)
        return render (request,'app/update.html',{'userfinal':userfinal})
    return render (request,'app/update.html',{'user':user,'alert':alert,})

@custom_login_required
def update2(request,pk):
    user1 = User.objects.get(pk=pk)
    alert=False
    if request.method == "POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        dob=request.POST.get('date','')
        city=request.POST.get('city','')
        course=request.POST.get('course','')
        post = User.objects.filter(pk=pk).first()
        post.name=name
        post.email=email
        post.phone=phone
        post.dob=dob
        post.city=city
        post.course=course
        post.save()
        if post:
            alert=True
            request.session['user'] = alert
        return redirect('update')
    request.session['user'] = alert         
    post=User.objects.all()
    return render (request,'app/update2.html',{'post':post,'user':user1,'alert':alert})
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            access_token = generate_access_token(user)
            response = redirect('studentview')
            response.set_cookie('access_token', access_token)
            return response
        else:
            return HttpResponse('Invalid credentials', status=401)
    return render(request, 'app/login.html')

@custom_login_required
def logout(request):
    response = redirect('login')
    response.delete_cookie('access_token')
    return response

@custom_login_required
def studentview(request):
    user=request.user
    return render(request, 'app/studentview.html',{'user':user})
    
