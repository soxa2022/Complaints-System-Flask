from flask import request
from flask_restful import Resource

from managers.complaint import ComplaintManager
from schemas.request_schema.complaints import ComplaintRequestSchema
from utils.decorators import validate_schema, permission_required


class ComplaintsResource(Resource):
    @auth.login_required
    @permission_required
    @validate_schema(ComplaintRequestSchema)
    def post(self):
        data = request.get_json()
        complaint = ComplaintManager.create_complaint(data)
        return ComplaintResponse().dump(complaint), 201
