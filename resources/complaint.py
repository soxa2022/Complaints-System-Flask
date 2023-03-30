from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.complaint import ComplaintManager
from models import RoleType
from schemas.request_schema.complaints import ComplaintRequestSchema
from schemas.response_schema.complaints import (
    ComplaintResponseSchema,
)
from utils.decorators import validate_schema, permission_required


class ComplaintsResource(Resource):
    @auth.login_required
    def get(self):
        complaints = ComplaintManager.get_complaints()
        if not complaints:
            return "Not Found Complaints"
        return ComplaintResponseSchema(many=True).dump(complaints)

    @auth.login_required
    @permission_required(RoleType.complainer)
    @validate_schema(ComplaintRequestSchema)
    def post(self):
        data = request.get_json()
        complaint = ComplaintManager.create_complaint(data)
        return ComplaintResponseSchema().dump(complaint), 201


class ComplaintApproveResource(Resource):
    @auth.login_required
    @permission_required(RoleType.approver)
    def get(self, pk):
        ComplaintManager.approve_complaint(pk)


class ComplaintRejectResource(Resource):
    @auth.login_required
    @permission_required(RoleType.approver)
    def get(self, pk):
        ComplaintManager.reject_complaint(pk)


class ComplaintResource(Resource):
    @auth.login_required
    @permission_required(RoleType.admin)
    def delete(self, pk):
        ComplaintManager.reject_complaint(pk)
