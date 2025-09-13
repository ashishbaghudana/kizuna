from . import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # This relationship links a User to all of their owned Contact records
    contacts = db.relationship('Contact', back_populates='owner', lazy=True)

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Foreign key to the User who owns this contact
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    # This relationship links a Contact back to its owner User object.
    # `back_populates` syncs this with the `contacts` relationship on the User model.
    owner = db.relationship('User', back_populates='contacts')
    
    events = db.relationship('Event', back_populates='contact', cascade="all, delete-orphan")
    interactions = db.relationship('Interaction', back_populates='contact', cascade="all, delete-orphan")

class EventType(db.Model):
    __tablename__ = 'event_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_date = db.Column(db.Date, nullable=True)
    
    contact_id = db.Column(UUID(as_uuid=True), db.ForeignKey('contacts.id'), nullable=False)
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_types.id'), nullable=False)
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    contact = db.relationship('Contact', back_populates='events')
    event_type = db.relationship('EventType')
    creator = db.relationship('User')

class Interaction(db.Model):
    __tablename__ = 'interactions'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interaction_date = db.Column(db.Date, nullable=False, default=datetime.date.today)
    notes = db.Column(db.Text)
    
    contact_id = db.Column(UUID(as_uuid=True), db.ForeignKey('contacts.id'), nullable=False)
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    contact = db.relationship('Contact', back_populates='interactions')
    creator = db.relationship('User')