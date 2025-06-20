from .models import Category, Course

def course_categories(request):
    categories = Category.objects.all()
    courses = Course.objects.all()
    return {'categories': categories, 'courses': courses}
