from datetime import datetime

from db import db


class TransactionModel(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.String(100), nullable=False)
    transfer_id = db.Column(db.String(100), nullable=False)
    custom_transfer_id = db.Column(db.String(150), nullable=False)
    target_account_id = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    complaint_id = db.Column(
        db.Integer, db.ForeignKey("complaints.id"), nullable=False, unique=True
    )
    complaint = db.relationship("Complaint")
