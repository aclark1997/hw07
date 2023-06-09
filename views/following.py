from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # return all of the "following" records that the current user is following
        print('test')
        following = Following.query.filter_by(user_id=self.current_user.id);
        return Response(json.dumps([followed.to_dict_following() for followed in following]), mimetype="application/json", status=200)

    def post(self):
        # create a new "following" record based on the data posted in the body 
        body = request.get_json()

        try:
            int(body.get('user_id'))
        except:
            return Response(json.dumps({}), mimetype="application/json", status=400)

        follow = Following(self.current_user.id, body.get('user_id'))

        users = User.query.filter(User.id==body.get('user_id'));
        try:
            user = [user.to_dict() for user in users][0]
        except:
            return Response(json.dumps({}), mimetype="application/json", status=404)

        try:
            db.session.add(follow)
            db.session.commit()
            return Response(json.dumps(follow.to_dict_following()), mimetype="application/json", status=201)
        except:
            return Response(json.dumps({}), mimetype="application/json", status=400)

class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # delete "following" record where "id"=id
        follow = Following.query.filter(Following.id == id)
        

        if follow.delete() == 0:
            return Response(json.dumps({}), mimetype="application/json", status=404)
                
        db.session.commit()
        return Response(json.dumps({}), mimetype="application/json", status=200)




def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<int:id>', 
        '/api/following/<int:id>/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
