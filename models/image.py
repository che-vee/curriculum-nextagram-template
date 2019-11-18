import peewee as pw

from config import Config
from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property

class Image(BaseModel):
    filename = pw.CharField(null=False)
    user = pw.ForeignKeyField(User, backref='images', on_delete='cascade')

    @hybrid_property
    def image_url(self):
        return 'https://' + Config.S3_LOCATION + self.filename