from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget

from blog.models import BlogPost, BlogCategory, Photo, Location
from ipware.ip import get_ip

class PhotoInline(admin.TabularInline):
    model = Photo 
    extra = 0 
    sortable_field_name = "position"


class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    """
    Admin class for blog posts.
    """
    list_display = ('title', 'admin_summery', 'view_count', 'comment_count', 'category', 'published', 'date_published')
    list_editable = ('category', 'published', 'date_published')
    list_filter = ("category", "published")
    search_fields = ("title", "content")
    readonly_fields = ('date_created', 'date_updated')
    date_hierarchy = "date_published"
    ordering = ("-date_published", )
    form = BlogPostForm
    inlines = [PhotoInline]

    def save_model(self, request, obj, form, change):
        ip = get_ip(request)
        if ip == '127.0.0.1':
            ip = '41.136.98.140'
        if ip:
            obj.save(ip)
        else:
            obj.save()

admin.site.register(BlogPost, BlogPostAdmin)


class BlogCategoryAdmin(admin.ModelAdmin):
    """
    Admin class for blog categories.
    """
    list_display = ('title', 'position')
    list_editable = ('position',)
    ordering = ('position', 'title')

admin.site.register(BlogCategory, BlogCategoryAdmin)


class PhotoAdmin(admin.ModelAdmin):
    #list_display = ('title', 'position', 'camera', 'date_taken', 'date_added', 'is_public', 'is_published', 'view_count', 'admin_thumbnail')
    list_display = ('title', 'post', 'position', 'is_public', 'is_published')
    list_filter = ['post', 'date_added', 'is_public', 'is_published']
    list_editable = ('position', 'is_public', 'is_published')
    search_fields = ['title', 'caption']
    list_per_page = 10

admin.site.register(Photo, PhotoAdmin)

admin.site.register(Location)


'''
class ArchiveAdmin(admin.ModelAdmin):
    """
    Admin class for blog categories.
    """
    list_display = ("year", "month", "post_count")
    ordering = ("year", "month")
    list_filter = ("year", "month", "post_count")

admin.site.register(Archive, ArchiveAdmin)
'''
