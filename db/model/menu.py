from tortoise import fields
from db.model.base import BaseModel


class Menu(BaseModel):
    list_label = fields.CharField(max_length=255)
    list_item = fields.JSONField()
    order = fields.IntField()

    class Meta:
        table = "menus"

    def __str__(self):
        return self.list_label
