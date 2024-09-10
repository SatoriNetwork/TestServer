# models.py
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from flask_restx import fields
from extensions import db  # Import db from extensions.py

class ProposalModel(db.Model):
    __tablename__ = 'proposals'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    proposal_date = db.Column(db.DateTime(timezone=True), nullable=False)
    complete_date = db.Column(db.DateTime(timezone=True))
    value = db.Column(db.Numeric(15, 2), nullable=False)
    image_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

class VoteModel(db.Model):
    __tablename__ = 'votes'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id = db.Column(UUID(as_uuid=True), db.ForeignKey('proposals.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), nullable=False)
    vote = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('proposal_id', 'user_id', name='uq_proposal_user'),)

# Define Swagger models
proposal_model = {
    'id': fields.String(required=True, description='Proposal ID'),
    'title': fields.String(required=True, description='Title of the proposal'),
    'description': fields.String(required=True, description='Description of the proposal'),
    'proposal_date': fields.DateTime(required=True, description='Date of the proposal'),
    'complete_date': fields.DateTime(description='Completion date of the proposal'),
    'value': fields.Float(required=True, description='Value of the proposal'),
    'image_url': fields.String(description='Image URL for the proposal'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last updated timestamp'),
}

vote_model = {
    'id': fields.String(required=True, description='Vote ID'),
    'proposal_id': fields.String(required=True, description='Proposal ID'),
    'user_id': fields.String(required=True, description='User ID'),
    'vote': fields.Boolean(required=True, description='Vote value'),
    'timestamp': fields.DateTime(description='Timestamp of the vote'),
}