from flask import Response, request
from flask_restful import Resource
from models import User
from views import get_authorized_user_ids
import json

class SuggestionsListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # suggestions should be any user with an ID that's not in this list:
        # print()
        #following = Following.query.filter_by(user_id=self.current_user.id);
        authed = get_authorized_user_ids(self.current_user)

        users = User.query.filter(id!=-1);
        users_filtered = []

        for user in users:
            if user not in authed and len(users_filtered) < 7 and user.id != self.current_user.id:
                users_filtered.append(user);

        return Response(json.dumps([user.to_dict() for user in users_filtered]), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint, 
        '/api/suggestions', 
        '/api/suggestions/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
