# models.py
# Separation of Concerns: Data models
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

db = SQLAlchemy()

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
