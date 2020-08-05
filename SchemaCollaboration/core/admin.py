from django.contrib import admin

from .models import Schema


class SchemaAdmin(admin.ModelAdmin):
    list_display = ('uuid',)
    ordering = ('uuid',)


admin.site.register(Schema, SchemaAdmin)
