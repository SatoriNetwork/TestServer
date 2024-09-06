
from flask import Flask, request, jsonify
from flask_restx import Resource, Api
from config import Config
from models import db
from schemas import ProposalSchema, VoteSchema

app = Flask(__name__)

# define routes, with the marshmallow schemas enforced/validation
api = Api(app)

# Register the models with Swagger
# api.models['Proposal'] = proposal_model
# api.models['Vote'] = vote_model

proposal_schema = ProposalSchema()
vote_schema = VoteSchema()

# Update the routes to use the Resource class


@api.route('/proposals')
class ProposalResource(Resource):
    @api.expect(proposal_schema)  # Add Swagger documentation for input
    def post(self):
        payload = request.json
        data = proposal_schema.load(payload.get('dto2'))
        return jsonify({"message": "Proposal created", "data": data}), 201


@api.route('/votes')
class VoteResource(Resource):
    @api.expect(vote_schema)  # Add Swagger documentation for input
    def post(self):
        data = vote_schema.load(request.json)
        return jsonify({"message": "Vote recorded", "data": data}), 201


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        threaded=True,
        debug=True,
        use_reloader=False)
