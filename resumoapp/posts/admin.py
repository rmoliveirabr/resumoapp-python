from django.contrib import admin
from .models import EducationGroup, EducationYear, EducationSubject, SubjectTopic, Post

class PostAdmin(admin.ModelAdmin):
    list_display = [ 'title', 'user', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register([EducationGroup, EducationYear, EducationSubject, SubjectTopic])
