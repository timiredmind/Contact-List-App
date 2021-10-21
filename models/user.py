from extension import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String, nullable=False, unique=True, index=True)
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    status = db.Column(db.Boolean, default=True)
    contacts = db.relationship("Contact", backref="user", lazy=True)

    @property
    def data(self):
        return {
            "username": self.username,
            "email": self.email,
            "phone_number": self.phone_number
        }

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_phone_number(cls, phone_number):
        return cls.query.filter_by(phone_number=phone_number).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
