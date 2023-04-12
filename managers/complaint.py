import os
import uuid

from flask import Response
from werkzeug.exceptions import BadRequest

from constans import TEMP_FILE_FOLDER
from db import db
from managers.auth import auth
from models import Complaint, RoleType, State, TransactionModel
from services.s3 import S3Service
from services.wise import WiseService
from utils.helper import decode_photo

wise_service = WiseService()
s3_service = S3Service()


class ComplaintManager:
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

        photo_into_str = complaint_data.pop("photo")
        extension = complaint_data.pop("extension")
        photo_name = f"{str(uuid.uuid4())}.{extension}"
        path_photo_file = os.path.join(TEMP_FILE_FOLDER, photo_name)
        decode_photo(path_photo_file, photo_into_str)
        try:
            url = s3_service.upload_file(path_photo_file, photo_name)
        except Exception as ex:
            raise Exception("Upload photo failed")
        finally:
            os.remove(path_photo_file)

        complaint_data["photo_url"] = url
        complaint = Complaint(**complaint_data)
        amount = complaint_data["amount"]
        full_name = f"{current_user.first_name} {current_user.last_name}"
        iban = current_user.iban
        db.session.add(complaint)
        db.session.flush()
        ComplaintManager.issue_transaction(amount, full_name, iban, complaint.id)

        db.session.commit()
        return complaint

    @staticmethod
    def approve_complaint(complaint_id):
        ComplaintManager.validate_status(complaint_id)
        transaction = TransactionModel.query.filter_by(
            complaint_id=complaint_id
        ).first()
        wise_service.fund_transfer(transaction.transfer_id)
        Complaint.query.filter_by(id=complaint_id).update({"status": State.approved})
        db.session.commit()

    @staticmethod
    def reject_complaint(complaint_id):
        ComplaintManager.validate_status(complaint_id)
        transaction = TransactionModel.query.filter_by(
            complaint_id=complaint_id
        ).first()
        wise_service.cancel_transfers(transaction.transfer_id)
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
        quote_id = wise_service.create_quote(amount)
        recipient_id = wise_service.create_recipient(full_name, iban)
        custom_trans_id = str(uuid.uuid4())
        transaction_id = wise_service.create_transfer(
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
        db.session.add(transaction)
        db.session.flush()


role_mapper = {
    RoleType.complainer: ComplaintManager.get_complainer_complaints,
    RoleType.admin: ComplaintManager.get_admin_complaints,
    RoleType.approver: ComplaintManager.get_approve_complaints,
}
