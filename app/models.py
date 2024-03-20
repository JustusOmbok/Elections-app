from app import db
from sqlalchemy import Column, String
# Define models
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.String(50), nullable=False)
    station = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)

class President(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    party_name = db.Column(db.String(100), nullable=False)
    party_color = Column(String(20), nullable=False)

class Governor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    party_name = db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(50), nullable=False)
    party_color = Column(String(20), nullable=False)

class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    national_id = db.Column(db.String(20), unique=True, nullable=False)
    county = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(128))  # New field for storing hashed passwords
    votes_president = db.relationship('Vote_president', backref='voter', lazy=True)
    votes_governor = db.relationship('Vote_governor', backref='voter', lazy=True)

class Vote_president(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    president_id = db.Column(db.Integer, db.ForeignKey('president.id'), nullable=False)
    voter_id = db.Column(db.Integer, db.ForeignKey('voter.id'), nullable=False)

class Vote_governor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    governor_id = db.Column(db.Integer, db.ForeignKey('governor.id'), nullable=False)
    voter_id = db.Column(db.Integer, db.ForeignKey('voter.id'), nullable=False)