from django.db import models

from core.models import CreateModifyOn
from core.models import Person


class AbstractComment(CreateModifyOn):
    author = models.ForeignKey(Person, null=False, blank=False, on_delete=models.PROTECT)
    text = models.TextField()
    private = models.BooleanField()

    class Meta:
        abstract = True


class Comment(AbstractComment):
    pass


class ToDo(AbstractComment):
    done = models.BooleanField()
    done_by = models.ForeignKey(Person, related_name='done_by_author', null=False, blank=False,
                                on_delete=models.PROTECT)
    done_on = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'TO DOs'