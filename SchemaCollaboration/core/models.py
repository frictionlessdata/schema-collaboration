import uuid as uuid_lib

from django.db import models
from django.urls import reverse


class CreateModifyOn(models.Model):
    """Details of data creation and modification: including date, time and user."""
    objects = models.Manager()  # Helps Pycharm CE auto-completion

    created_on = models.DateTimeField(help_text='Date and time at which the entry was created', auto_now_add=True,
                                      blank=False, null=False)
    modified_on = models.DateTimeField(help_text='Date and time at which the entry was modified', auto_now=True,
                                       blank=True, null=True)

    class Meta:
        abstract = True


class Person(CreateModifyOn):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=128, unique=True)

    def get_absolute_url(self):
        return reverse('management:person-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = 'People'


class DatapackageStatus(CreateModifyOn):
    name = models.CharField(max_length=500, null=False, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Datapackage statuses'


class Datapackage(CreateModifyOn):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False, unique=True)
    schema = models.TextField(editable=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    collaborators = models.ManyToManyField(Person, blank=True)
    status = models.ForeignKey(DatapackageStatus, null=True, blank=True, on_delete=models.PROTECT)

    def collaborators_str(self):
        return ', '.join([collaborator.full_name for collaborator in self.collaborators.all().order_by('full_name')])

    def get_absolute_url(self):
        return reverse('datapackage-detail', kwargs={'uuid': str(self.uuid)})

    def __str__(self):
        return self.name
