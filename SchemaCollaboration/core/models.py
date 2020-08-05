import uuid as uuid_lib

from django.db import models


class Schema(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False, unique=True)
    schema = models.BinaryField()  # TODO: move it to a file
