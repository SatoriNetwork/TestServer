
from flask_restx import fields

def create_swagger_models(api):
    proposal_model = api.model('Proposal', {
        'id': fields.String(description='The unique identifier for the proposal'),
        'title': fields.String(required=True, description='The title of the proposal'),
        'description': fields.String(required=True, description='A detailed description of the proposal'),
        'proposal_date': fields.DateTime(required=True, description='The date when the proposal was submitted'),
        'complete_date': fields.DateTime(description='The date when the proposal was completed or closed'),
        'value': fields.String(required=True, description='The monetary value or cost associated with the proposal'),
        'image_url': fields.String(description='URL to an image related to the proposal'),
        'yes_votes': fields.Integer(description='The number of yes votes for this proposal'),
        'no_votes': fields.Integer(description='The number of no votes for this proposal')
    })

    vote_model = api.model('Vote', {
        'proposal_id': fields.String(required=True, description='The unique identifier of the proposal being voted on'),
        'user_id': fields.String(required=True, description='The unique identifier of the user casting the vote'),
        'vote': fields.Boolean(required=True, description='The vote: True for Yes, False for No')
    })

    return {
        'Proposal': proposal_model,
        'Vote': vote_model
    }