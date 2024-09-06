from flask_restx import Resource, fields
from flask import request
from services import get_proposals, submit_vote
from schemas import ProposalSchema, VoteSchema
from marshmallow import ValidationError

def register_routes(api):
    # Use Marshmallow schemas to generate Flask-RESTX models
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

    @api.route('/proposals')
    class ProposalList(Resource):
        @api.doc('list_proposals', 
                 description='Retrieves a list of all proposals with their vote counts.',
                 responses={
                     200: 'Success',
                     500: 'Internal Server Error'
                 })
        @api.marshal_list_with(proposal_model)
        def get(self):
            """List all proposals"""
            proposals = get_proposals()
            return ProposalSchema(many=True).dump(proposals)

    @api.route('/votes')
    class VoteSubmission(Resource):
        @api.doc('submit_vote', 
                 description='Submit a vote for a specific proposal.',
                 responses={
                     200: 'Vote submitted successfully',
                     400: 'Invalid vote submission',
                     500: 'Internal Server Error'
                 })
        @api.expect(vote_model)
        @api.response(200, 'Vote submitted successfully')
        @api.response(400, 'Invalid vote submission')
        def post(self):
            """Submit a vote for a proposal"""
            vote_schema = VoteSchema()
            try:
                data = vote_schema.load(request.json)
                success, message = submit_vote(data['proposal_id'], data['user_id'], data['vote'])
                if success:
                    return {"message": message}, 200
                else:
                    return {"error": message}, 400
            except ValidationError as e:
                return {"error": str(e)}, 400