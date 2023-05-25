from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("pk", "create_date", "update_date")
    exclude = ("likes",)


class CommentAdmin(admin.TabularInline):
    model = Comment
    extra = 0


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
