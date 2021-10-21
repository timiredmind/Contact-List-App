from extension import db
from flask_jwt_extended import get_jwt, get_jwt_identity


class TokenBlockList(db.Model):
    __tablename__= "token_block_list"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String, nullable=False, unique=True)
    user = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

