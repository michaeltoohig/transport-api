# project/models/vehicle.py

from datetime import datetime
from flask import current_app
from project import db, bcrypt
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID


class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plate = db.Column(db.String(12), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationships
    images = db.relationship("VehicleImage", back_populates("vehicle"))
    votes = db.relationship("VehicleVote", back_populates="vehicle")

    def __init__(self, plate: str, created_at:datetime=datetime.utcnow()):
        self.plate = plate
        self.created_at = created_at

    @staticmethod
    def first_by(**kwargs):
        """Get first db entity that match to criterium"""
        return Vehicle.query.filter_by(**kwargs).first()

    def first(*criterion):
        """Get first db entity that match to criterium"""
        return Vehicle.query.filter(*criterion).first()

    @staticmethod
    def get(plate: str):
        """Get db entity that match the plate"""
        return Vehicle.query.get(plate)


class VehicleVote(db.Model):
    """
    A vote for a vehicle. Either positive or negative.
    A vote shall not be changed far into the future to create a vehicle's vote history.
    """
    __tablename__ = "votes_vehicles"

    vote = db.Column(db.SmallInteger, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Relationships
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), primary_key=True)
    vehicle = db.relationship("Vehicle", back_populates="votes")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship("User", back_populates="votes")


class VehicleImage(db.Model):
    __tablename__ = "images_vehicles"
    
    key = db.Column(UUID)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    vehicle_id =db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    vehicle = db.relationship("Vehicle", back_populates="sightings")
    

    def __init__(self, username: str, email: str, password:str=None, cellphone_number:str=None, cellphone_cc:str=None,
                 email_validation_date=None, fb_id:str=None, fb_access_token:str=None, cellphone_validation_code:str=None,
                 cellphone_validation_code_expiration:datetime=None,
                 cellphone_validation_date:datetime=None, roles:UserRole=UserRole.USER, created_at:datetime=datetime.utcnow()):
        self.username = username
        self.email = email

    @staticmethod
    def first_by(**kwargs):
        """Get first db entity that match to criterium"""
        return User.query.filter_by(**kwargs).first()

    def first(*criterion):
        """Get first db entity that match to criterium"""
        return User.query.filter(*criterion).first()

    @staticmethod
    def get(id: int):
        """Get db entity that match the id"""
        return User.query.get(id)
