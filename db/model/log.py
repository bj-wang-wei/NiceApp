from tortoise import fields
from db.model.base import BaseModel



class Log(BaseModel):
    log_text = fields.TextField()
    level = fields.CharField(max_length=255)
    username = fields.CharField(max_length=255)
    class Meta:
        table = "logs"

    def __str__(self):
        return self.log_text
