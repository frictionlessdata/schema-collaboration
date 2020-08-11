from django.contrib import admin

from .models import Schema


class SchemaAdmin(admin.ModelAdmin):
    search_fields = ('uuid', 'schema',)
    list_display = ('uuid', 'created_on', 'modified_on', 'schema',)
    ordering = ('uuid',)
    readonly_fields = ('uuid', 'created_on', 'modified_on',)


admin.site.register(Schema, SchemaAdmin)
