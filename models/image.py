# import peewee as pw

# from models.base_model import BaseModel
# from models.user import User
# from playhouse.hybrid import hybrid_property

# class Image(BaseModel):
#     filename = pw.CharField()
#     user = pw.ForeignKeyField(User, backref="")

#     @hybrid_property
#     image_url(self):
#         return 'https://' + Config.S3_LOCATION + self.filename