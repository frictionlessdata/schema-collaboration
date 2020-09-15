from django.contrib import admin

from .models import Datapackage, Person, DatapackageStatus


class SchemaAdmin(admin.ModelAdmin):
    search_fields = ('uuid', 'name', 'schema',)
    list_display = ('uuid', 'name', 'collaborator_names', 'created_on', 'modified_on', 'schema',)
    ordering = ('uuid',)
    readonly_fields = ('uuid', 'created_on', 'modified_on',)

    def collaborator_names(self, obj):
        names = ', '.join([collaborator.full_name for collaborator in obj.collaborators.all()])

        return names


class PersonAdmin(admin.ModelAdmin):
    search_fields = ('uuid', 'full_name', 'user__username', )
    list_display = ('uuid', 'full_name', 'user', 'created_on', 'modified_on',)
    readonly_fields = ('uuid', 'created_on', 'modified_on',)


class DatapackageStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on', 'modified_on',)
    search_fields = ('name',)


admin.site.register(Datapackage, SchemaAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(DatapackageStatus, DatapackageStatusAdmin)
