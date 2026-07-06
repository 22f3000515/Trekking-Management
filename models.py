from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#users model
db=SQLAlchemy()
class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    role=db.Column(db.String(10),nullable=False)
    phone=db.Column(db.String(15))
    experience=db.Column(db.Integer,default=0)
    status=db.Column(db.String(20),default="approved")
    is_blacklisted=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    bookings=db.relationship('Booking',backref='user',lazy=True)
    reviews=db.relationship("Review",backref='user',lazy=True)
    
#treks model
class Trek(db.Model):
    __tablename__ = "treks"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    location=db.Column(db.String(100),nullable=False)
    country=db.Column(db.String(50),nullable=False)
    is_international=db.Column(db.Boolean,default=False)
    category=db.Column(db.String(20),nullable=False)
    difficulty=db.Column(db.String(20),nullable=False)
    duration_days=db.Column(db.Integer,nullable=False)
    description=db.Column(db.Text)
    price=db.Column(db.Float,default=0.0)
    total_slots=db.Column(db.Integer,nullable=False)
    available_slots=db.Column(db.Integer,nullable=False)
    assigned_staff_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='open')
    start_date=db.Column(db.DateTime,nullable=False)
    end_date=db.Column(db.DateTime,nullable=False)
    best_season=db.Column(db.String(20))
    image=db.Column(db.String(200))
    description=db.Column(db.Text)
    created_at=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    assigned_staff=db.relationship(
        'User',foreign_keys=[assigned_staff_id],backref='assigned_treks',lazy=True)
    
    bookings=db.relationship('Booking',backref='trek',lazy=True)
    reviews=db.relationship('Review',backref='trek',lazy=True)

#bookings model
class Booking(db.Model):
    __tablename__="bookings"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    trek_id=db.Column(db.Integer,db.ForeignKey('treks.id'),nullable=False)
    booking_date=db.Column(db.DateTime,default=datetime.utcnow)
    participants_count=db.Column(db.Integer,nullable=False,default=1)
    status=db.Column(db.String(20),default="Booked")
    total_price=db.Column(db.Float,default=0.0)

#reviews model
class Review(db.Model):
    __tablename__="reviews" 
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    trek_id=db.Column(db.Integer,db.ForeignKey('treks.id'),nullable=False)
    comment=db.Column(db.Text)
    rating=db.Column(db.Integer,nullable=False) 
    created_at=db.Column(db.DateTime,default=datetime.utcnow)


