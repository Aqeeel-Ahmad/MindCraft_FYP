from django.contrib import admin
from .models import *


# Register your models here.

class WhatYouWillLearnTabularInline(admin.TabularInline):
    model = WhatYouWillLearn
    
class RequirementsTabularInline(admin.TabularInline):
    model = Requirements
    
    
class VideoTabularInline(admin.TabularInline):
    model = Video


class courseAdmin(admin.ModelAdmin):
    inlines = [WhatYouWillLearnTabularInline, RequirementsTabularInline, VideoTabularInline]

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Course, courseAdmin)
admin.site.register(Level)
admin.site.register(WhatYouWillLearn)
admin.site.register(Requirements)
admin.site.register(Lesson)
admin.site.register(Language)
admin.site.register(UserCourse)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'course_title', 'amount', 'paypal_order_id', 'payment_status', 'created_at']
    search_fields = ['paypal_order_id', 'payer_email', 'course_title']

