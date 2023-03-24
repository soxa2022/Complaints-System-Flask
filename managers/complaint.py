import uuid

from werkzeug.exceptions import BadRequest

from db import db
from managers.auth import auth
from models import Complaint, RoleType, State, TransactionModel
from services.wise import WiseService
from utils.decorators import validate_complaint_id


class ComplaintManager:
    wise_service = WiseService()

    @staticmethod
    def get_complaints():
        current_user = auth.current_user()
        role = current_user.role
        complaints = role_mapper[role]()
        return complaints

    @staticmethod
    def get_complainer_complaints():
        current_user = auth.current_user()
        return Complaint.query.filter_by(user_id=current_user.id).all()

    @staticmethod
    def get_approve_complaints():
        return Complaint.query.filter_by(status=State.pending).all()

    @staticmethod
    def get_admin_complaints():
        return Complaint.query.filter_by().all()

    @staticmethod
    def create_complaint(complaint_data):
        current_user = auth.current_user()
        complaint_data["user_id"] = current_user.id
        complaint = Complaint(**complaint_data)
        amount = complaint_data["amount"]
        full_name = f"{current_user.first_name} {current_user.last_name}"
        iban = current_user.iban
        db.session.add(complaint)
        db.session.flush()
        transaction = ComplaintManager.issue_transaction(
            amount, full_name, iban, complaint.id
        )
        db.session.add(transaction)
        db.session.flush()
        db.session.commit()

    @staticmethod
    def approve_complaint(complaint_id):
        ComplaintManager.validate_status(complaint_id)
        transaction = TransactionModel.query.filter_by(
            complaint_id=complaint_id
        ).first()
        ComplaintManager.wise_service.fund_transfer(transaction.transfer_id)
        Complaint.query.filter_by(id=complaint_id).update({"status": State.approved})
        db.session.commit()

    @staticmethod
    def reject_complaint(complaint_id):
        ComplaintManager.validate_status(complaint_id)
        transaction = TransactionModel.query.filter_by(
            complaint_id=complaint_id
        ).first()
        ComplaintManager.wise_service.cancel_transfers(transaction.transfer_id)
        Complaint.query.filter_by(id=complaint_id).update({"status": State.rejected})
        db.session.commit()

    @staticmethod
    def validate_status(complaint_id):
        complaint = Complaint.query.filter_by(id=complaint_id).first()
        if not complaint:
            raise BadRequest("Complaint not exist")
        if not complaint.status == State.pending:
            raise BadRequest("Can not change processed complaint")

    @staticmethod
    def issue_transaction(amount, full_name, iban, complaint_id):
        quote_id = ComplaintManager.wise_service.create_quote(amount)
        recipient_id = ComplaintManager.wise_service.create_recipient(full_name, iban)
        custom_trans_id = str(uuid.uuid4())
        transaction_id = ComplaintManager.wise_service.create_transfer(
            quote_id, recipient_id, custom_trans_id
        )
        transaction = TransactionModel(
            quote_id=quote_id,
            transfer_id=transaction_id,
            custom_transfer_id=custom_trans_id,
            target_account_id=recipient_id,
            amount=amount,
            complaint_id=complaint_id,
        )
        return transaction


role_mapper = {
    RoleType.complainer: ComplaintManager.get_complainer_complaints,
    RoleType.admin: ComplaintManager.get_admin_complaints,
    RoleType.approver: ComplaintManager.get_approve_complaints,
}
