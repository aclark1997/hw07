from flask import Response, request
from flask_restful import Resource
from models import LikePost, Post, db
import json

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        # create a new "like_post" based on the data posted in the body 
        body = request.get_json()
        #LikePost.query.filter(LikePost.id==0)

        try:
            int(body.get('post_id'))
        except:
            return Response(json.dumps({}), mimetype="application/json", status=400)

        posts = Post.query.filter(Post.id==body.get('post_id'));
        try:
            post = [post.to_dict() for post in posts][0]
        except:
            return Response(json.dumps({}), mimetype="application/json", status=404)

        like = LikePost(self.current_user.id, body.get('post_id'))
        
        try:
            db.session.add(like)
            db.session.commit()
            return Response(json.dumps(like.to_dict()), mimetype="application/json", status=201)
        except:
            return Response(json.dumps({}), mimetype="application/json", status=400)
        

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        like = LikePost.query.filter(Post.id == id)
        

        if like.delete() == 0:
            return Response(json.dumps({}), mimetype="application/json", status=404)
                
        db.session.commit()
        return Response(json.dumps({}), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/likes', 
        '/api/posts/likes/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/likes/<int:id>', 
        '/api/posts/likes/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
