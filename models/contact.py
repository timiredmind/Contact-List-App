from extension import db
from sqlalchemy import asc, desc

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



    @classmethod
    def get_by_contact_id(cls, contact_id):
        return cls.query.filter_by(id=contact_id).first()

    @classmethod
    def get_all_by_user(cls, user_id, page, per_page):
        return cls.query.filter_by(user_id=user_id, status=True)\
            .order_by(asc(cls.date_created)).paginate(page=page, per_page=per_page)# Returns a paginated object


