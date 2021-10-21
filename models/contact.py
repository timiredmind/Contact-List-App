from extension import db


class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    image_url = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.Boolean, default=True)

    @property
    def data(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "image_url": self.image_url
        }

    @classmethod
    def get_by_contact_id(cls, contact_id):
        return cls.query.filter_by(id=contact_id).first()

