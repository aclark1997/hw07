from flask import Response, request
from flask_restful import Resource
import json
from models import db, Comment, Post

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        # create a new "Comment" based on the data posted in the body 
        body = request.get_json()
            
        try:
            int(body.get('post_id'))
        except:
            return Response(json.dumps({}), mimetype="application/json", status=400)

        posts = Post.query.filter(Post.id==body.get('post_id'));
        try:
            post = [post.to_dict() for post in posts][0]
        except:
            return Response(json.dumps({}), mimetype="application/json", status=404)

        if body.get('text') == None:
            return Response(json.dumps({}), mimetype="application/json", status=400)

        new_comment = Comment(
            text=body.get('text'),
            user_id=self.current_user.id,
            post_id=body.get('post_id'),
        )

        db.session.add(new_comment)
        db.session.commit()
        return Response(json.dumps(new_comment.to_dict()), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    def delete(self, id):
        # delete "Comment" record where "id"=id
        comment = Comment.query.filter(Comment.id == id)
        
        try:
            int(id)
        except:
            return Response(json.dumps({}), mimetype="application/json", status=404)

        posts = Post.query.filter(Post.id==id);
        try:
            post = [post.to_dict() for post in posts][0]
        except:
            return Response(json.dumps({}), mimetype="application/json", status=404)

        if comment.delete() == 0:
            return Response(json.dumps({}), mimetype="application/json", status=404)
                
        db.session.commit()
        return Response(json.dumps({}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': api.app.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<int:id>', 
        '/api/comments/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
