import uuid as uuid_lib

from django.db import models


class CreateModifyOn(models.Model):
    """Details of data creation and modification: including date, time and user."""
    objects = models.Manager()  # Helps Pycharm CE auto-completion

    created_on = models.DateTimeField(help_text='Date and time at which the entry was created', auto_now_add=True,
                                      blank=False, null=False)
    modified_on = models.DateTimeField(help_text='Date and time at which the entry was modified', auto_now=True,
                                       blank=True, null=True)

    class Meta:
        abstract = True


class Schema(CreateModifyOn):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False, unique=True)
    schema = models.BinaryField()  # TODO: move it to a file

    def schema_text(self):
        return self.schema.decode('utf-8')
