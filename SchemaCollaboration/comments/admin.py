from django.contrib import admin

from comments.models import Comment, ToDo


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'private', 'created_on', 'modified_on',)
    search_fields = ('author', 'text',)


class ToDoAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'private', 'done', 'done_by', 'done_on', 'created_on', 'modified_on',)
    search_fields = ('author', 'text',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(ToDo, ToDoAdmin)
