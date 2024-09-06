# schemas.py
# Separation of Concerns: Data serialization/deserialization
# Using Marshmallow for data serialization and validation
from marshmallow import Schema, fields, post_load
from datetime import datetime
import uuid

class ProposalSchema(Schema):
    id = fields.UUID(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    proposal_date = fields.DateTime(required=True)
    complete_date = fields.DateTime(allow_none=True)
    value = fields.Decimal(required=True, as_string=True)
    image_url = fields.Url(allow_none=True)
    yes_votes = fields.Int(dump_only=True)
    no_votes = fields.Int(dump_only=True)

class VoteSchema(Schema):
    id = fields.UUID(dump_only=True)
    proposal_id = fields.UUID(required=True)
    user_id = fields.UUID(required=True)
    vote = fields.Boolean(required=True)
    timestamp = fields.DateTime(dump_only=True)