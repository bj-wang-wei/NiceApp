from tortoise import fields
from db.model.base import BaseModel

class Role(BaseModel):
    name = fields.CharField(max_length=255, unique=True)
    permissions = fields.JSONField()
    class Meta:
        table = "roles"

    def __str__(self):
        return self.name
