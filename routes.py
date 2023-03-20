from resources.auth import RegisterResource, LoginResource
from resources.complaint import ComplaintsResource

routes = (
    (RegisterResource, "/register"),
    (LoginResource, "/login"),
    (ComplaintsResource, "/complaints"),
)
