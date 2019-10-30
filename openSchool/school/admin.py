from django.contrib import admin
from school.models import *
# Register your models here.
admin.site.site_header = 'brocode administration'
class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseTitle','courseDescription','hours')
    search_fields = ('courseTitle',)

    class Media:
        css : { "screen" : ("../admin/css/forms.css")}

admin.site.register(Course,CourseAdmin)
admin.site.register(Weeks)
admin.site.register(Contact)
admin.site.register(ExtendUser)

