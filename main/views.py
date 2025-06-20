from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from main.models import Category, Course, Level, Video, UserCourse, Order
from django.template.loader import render_to_string
from django.http import JsonResponse
import json
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

def base(request):
    return render(request, 'base.html')

def home(request):
    categories = Category.objects.all().order_by('id')[0:5]
    courses = Course.objects.filter(status= 'PUBLISH').order_by('-id')
    
    
    context= {
        'categories' : categories,
        'courses' : courses,
        
    }
    return render(request, 'main/home.html', context)

def single_course(request):
    categories = Category.get_all_category(Category)
    level = Level.objects.all()
    course = Course.objects.all()
    FreeCourse_count= Course.objects.filter(price=0).count()
    PaidCourse_count= Course.objects.filter(price__gte=1).count()
    
    context = {
        'categories' : categories,
        'level' : level,
        'course' : course,
        'FreeCourse_count': FreeCourse_count,
        'PaidCourse_count': PaidCourse_count,
    }
    return render(request, 'main/single_course.html', context)

def filter_data(request):
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    
    if price == ['PriceFree']:
        course = Course.objects.filter(price=0)
    elif price == ['PricePaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['PriceAll']:
        course = Course.objects.all()
    elif category:
        course = Course.objects.filter(category__id__in= category).order_by('-id')
    elif level:
        course= Course.objects.filter(level__id__in = level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')
        
    context= {
        'course': course
    }
    
    t=render_to_string('ajax/course.html',context)
    return JsonResponse({'data': t})



def contact_us(request):
    
    return render(request, 'main/contact_us.html')



def about_us(request):
    
    return render(request, 'main/about_us.html')



def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # check enmial
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists!')
            return redirect('register')
        
        # check username
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'User Name already exists!')
            return redirect('register')
        user= User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return redirect('login')  
    return render(request, 'registration/register.html')



def profile(request):
    return render(request, 'profile.html')  # Your profile page



@login_required
def enrolled_courses(request):
    return render(request, 'enrolled_courses.html')  # List of enrolled courses



def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home after logging out




def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # If already logged in, redirect to home

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            # Authenticate user with username and password
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
        except User.DoesNotExist:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})

    return render(request, 'registration/login.html')



def update_profile(request):
    return render(request,'registration/update_profile.html')



def updated_profile(request):
    if request.method == "POST":
        username = request.POST.get('username')
        firs_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id
        
        user = User.objects.get(id=user_id)
        user.first_name = firs_name
        user.last_name = last_name
        user.username = username
        user.email = email
        
        if password != None and password != "":
            user.set_password(password)
        
        user.save()
        messages.success(request, "Profile Successfully Updated.")
        return redirect('update_profile')
    
    
def search_course(request):
    query = request.GET['query']
    course = Course.objects.filter(title__icontains=query)
    
    context = {
        'course': course,
    }
    return render(request, 'search/search.html',context) 



def course_details(request, slug):
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))
    
    course_id = Course.objects.get(slug=slug).id
    try:
        check_enrolled = UserCourse.objects.get(user=request.user, course__id=course_id)
    except UserCourse.DoesNotExist:
        check_enrolled = None
    
    course = Course.objects.filter(slug=slug)
    
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    
    context= {
        'course' : course,
        'time_duration' : time_duration,
        'check_enrolled' : check_enrolled,
        
    }
    return render(request, 'course/course_details.html', context)



def page_not_found(request):
    return render(request, 'error/404.html')

def checkout(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if course.price == 0:
        course = UserCourse(
            user = request.user,
            course = course,
        )
        course.save()
        messages.success(request, "You have successfully enrolled in the course.")
        return redirect('my_courses')
    
    context = {
        'course' : course,
    }
    return render(request, 'checkout/checkout.html', context )

def my_courses(request):
    courses = UserCourse.objects.filter(user=request.user)    
    context = {
        'courses': courses,
    }
    return render(request, 'course/my-course.html', context)


def verify_payment(request):
    return render(request, 'checkout/payment_success.html')

def cancel_payment(request):
    return render(request, 'checkout/payment_cancel.html')

@csrf_exempt
def save_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order = Order.objects.create(
            user=request.user,
            course_title=data['courseTitle'],
            amount=data['amount'],
            paypal_order_id=data['orderID'],
            payer_email=data['payerEmail'],
            payment_status=data['status']
        )
        return JsonResponse({'message': 'Order saved!'}, status=200)      

