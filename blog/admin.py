from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment


class CommentInline(admin.StackedInline):
    # Inline shows the comment(s) when looking at the Post
    model = Comment
    extra = 0


# class PostAdmin(admin.ModelAdmin):
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = ("title", "slug", "status", "created_on")
    list_filter = ("status",)
    search_fields = [
        "title",
        "content",
    ]
    prepopulated_fields = {"slug": ("title",)}
    # The next line is to show the comment(s), when selecting a post
    inlines = [
        CommentInline,
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "body",
        "post",
        "created_on",
        "active",
    )
    list_filter = (
        "active",
        "created_on",
    )
    search_fields = (
        "name",
        "email",
        "body",
    )
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
