from models import RoleType
from test.base import TestAPIBase, generate_token
from test.factories import UserFactory


class TestAuthorizationAndPermissionRequirements(TestAPIBase):

    def test_auth_requirements(self):
        methods = {
            "GET": self.client.get,
            "POST": self.client.post,
            "PUT": self.client.put,
            "DELETE": self.client.delete
        }
        all_urls = [
            ("GET", "/complaints"),
            ("POST", "/complaints"),
            ("GET", "/complaints/1/approve"),
            ("GET", "/complaints/1/reject"),
        ]
        for method, url in all_urls:
            result = methods[method](url)
            assert result.status_code == 401
            assert result.json == {"message": "Invalid or missing token"}

    def test_permission__required_create_complaint_requires_complainer(self):

        # Testing approver user
        user = UserFactory(role=RoleType.approver)
        token = generate_token(user)
        headers = {"Authorization": f"Bearer {token}"}
        result = self.client.post("/complaints", headers=headers)
        assert result.status_code == 403
        assert result.json == {"message": "You not have permission to access this"}

        # Testing admin user too
        user = UserFactory(role=RoleType.admin)
        token = generate_token(user)
        headers = {"Authorization": f"Bearer {token}"}
        result = self.client.post("/complaints", headers=headers)
        assert result.status_code == 403
        assert result.json == {"message": "You not have permission to access this"}

        # Testing complainer user too
        user = UserFactory(role=RoleType.complainer)
        token = generate_token(user)
        headers = {"Authorization": f"Bearer {token}"}
        result = self.client.post("/complaints", headers=headers)
        assert result.status_code == 400

    def test_permission_required_approve_reject_complaint(self):
        # Testing admin user
        user = UserFactory(role=RoleType.admin)
        token = generate_token(user)
        headers = {"Authorization": f"Bearer {token}"}
        result = self.client.get("/complaints/1/approve", headers=headers)
        assert result.status_code == 403
        assert result.json == {"message": "You not have permission to access this"}

        # Testing complainer user
        user = UserFactory(role=RoleType.complainer)
        token = generate_token(user)
        headers = {"Authorization": f"Bearer {token}"}
        result = self.client.get("/complaints/1/reject", headers=headers)
        assert result.status_code == 403
        assert result.json == {"message": "You not have permission to access this"}

        # Testing approver user
        user = UserFactory(role=RoleType.approver)
        token = generate_token(user)
        headers = {"Authorization": f"Bearer {token}"}
        result = self.client.get("/complaints/1/reject", headers=headers)
        assert result.status_code == 400

