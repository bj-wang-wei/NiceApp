from tortoise import fields
from db.model.base import BaseModel
class User(BaseModel):
    username = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)
    mobile = fields.CharField(max_length=255, null=True)
    email = fields.CharField(max_length=255, null=True)
    avatar = fields.CharField(max_length=255, null=True)
    is_admin = fields.BooleanField(default=False)
    role = fields.ForeignKeyField("models.Role", related_name="users",null=True,on_delete= fields.OnDelete.SET_NULL)
    class Meta:
        table = "users"
        
    def __str__(self):
        return self.name
