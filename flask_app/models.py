from flask_login import UserMixin
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


class ConsumerUser(db.Document):
    idCode = db.StringField(required=True)


class BusinessUser(db.Document):
    companyName = db.StringField(required=True)
    stockCode = db.StringField()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    type = db.StringField(required=True)
    detail = db.GenericReferenceField(required=True)

    def get_id(self):
        return str(self.id)
