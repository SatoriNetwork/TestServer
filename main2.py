# main.py

from flask import Flask, request, jsonify
from flask_restx import Resource, Api
from marshmallow import ValidationError
from config import Config
from schemas import ProposalSchema, VoteSchema

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-RESTX
api = Api(app, version='1.0', title='Proposal API', description='API for managing proposals and votes')

# Initialize schemas
proposal_schema = ProposalSchema()
vote_schema = VoteSchema()

# API Resources
@api.route('/proposals')
class ProposalResource(Resource):
    @api.expect(api.model('Proposal', proposal_schema.fields))
    @api.response(201, 'Proposal created')
    @api.response(400, 'Validation error')
    def post(self):
        try:
            payload = request.json
            data = proposal_schema.load(payload.get('dto2', {}))
            # Here you would typically save the proposal to a database
            return {"message": "Proposal created", "data": data}, 201
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

@api.route('/votes')
class VoteResource(Resource):
    @api.expect(api.model('Vote', vote_schema.fields))
    @api.response(201, 'Vote recorded')
    @api.response(400, 'Validation error')
    def post(self):
        try:
            data = vote_schema.load(request.json)
            # Here you would typically save the vote to a database
            return {"message": "Vote recorded", "data": data}, 201
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        threaded=True,
        debug=True,
        use_reloader=False
    )