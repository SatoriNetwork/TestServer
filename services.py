from models import ProposalModel, VoteModel
from schemas import ProposalSchema, VoteSchema
from extensions import db

def get_proposals():
    proposals = ProposalModel.query.all()
    result = []
    for proposal in proposals:
        proposal_data = {
            'id': proposal.id,
            'title': proposal.title,
            'description': proposal.description,
            'proposal_date': datetime.fromisoformat(proposal.proposal_date) if isinstance(proposal.proposal_date, str) else proposal.proposal_date,
            'complete_date': datetime.fromisoformat(proposal.complete_date) if isinstance(proposal.complete_date, str) else proposal.complete_date,
            'value': proposal.value,
            'image_url': proposal.image_url,
            'yes_votes': VoteModel.query.filter_by(proposal_id=proposal.id, vote=True).count(),
            'no_votes': VoteModel.query.filter_by(proposal_id=proposal.id, vote=False).count()
        }
        result.append(proposal_data)
    return result
def submit_vote(proposal_id, user_id, vote):
    new_vote = VoteModel(
        proposal_id=proposal_id,
        user_id=user_id,
        vote=vote
    )
    db.session.add(new_vote)
    try:
        db.session.commit()
        return True, "Vote submitted successfully"
    except Exception as e:
        db.session.rollback()
        return False, str(e)