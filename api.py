from flask_restx import Resource
from flask import request
from services import get_proposals, submit_vote
from schemas import ProposalSchema, VoteSchema
from marshmallow import ValidationError
from swagger_models import create_swagger_models

def register_routes(api):
    swagger_models = create_swagger_models(api)

    @api.route('/test')
    class TestConnection(Resource):
        @api.doc('test_connection',
                 description='Test the API connection',
                 responses={
                     200: 'API is working correctly',
                 })
        def get(self):
            """Test the API connection"""
            return {"message": "API is working correctly", "status": "success"}, 200

    @api.route('/proposals')
    class ProposalList(Resource):
        @api.doc('list_proposals',
                 description='Retrieves a list of all proposals with their vote counts.',
                 responses={
                     200: 'Success',
                     500: 'Internal Server Error'
                 })
        @api.marshal_list_with(swagger_models['Proposal'])
        def get(self):
            """List all proposals"""
            proposals = get_proposals()
            return ProposalSchema(many=True).dump(proposals)

    @api.route('/proposal_votes')
    class VoteSubmission(Resource):
        @api.doc('submit_vote',
                 description='Submit a vote for a specific proposal.',
                 responses={
                     200: 'Vote submitted successfully',
                     400: 'Invalid vote submission',
                     500: 'Internal Server Error'
                 })
        @api.expect(swagger_models['Vote'])
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