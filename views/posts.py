from flask import Response, request
from flask_restful import Resource
from models import Post, Following, db
from views import get_authorized_user_ids

import json

def get_path():
    return request.host_url + 'api/posts/'

class PostListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    def get(self):
        # get posts created by one of these users:
        following = Following.query.filter_by(user_id=self.current_user.id);
        friend_ids = [];
        if request.args.get('limit') == None:
            limit = 20;
        for rec in following:
            friend_ids.append(rec.following_id);
        friend_ids.append(self.current_user.id);
        if request.args.get('limit') != None:
            try:
                limit = int(request.args.get('limit')) or 20
            except:
                return Response(json.dumps({'error': 'No strings, dude!'}), status=400)
        
        if(limit > 20):
            return Response(json.dumps({'error': 'Exceeded limit!'}), status=400)
        posts = Post.query.filter(Post.user_id.in_(friend_ids)).limit(limit);
        return Response(json.dumps([post.to_dict() for post in posts]), mimetype="application/json", status=200)

    def post(self):
        # create a new post based on the data posted in the body 
        body = request.get_json()

        if body == {}:
            return Response(json.dumps({}), mimetype="application/json", status=400)

        new_post = Post(
            image_url = body.get('image_url'),
            user_id=self.current_user.id,
            caption=body.get('caption'),
            alt_text=body.get('alt_text')
        )

        db.session.add(new_post)
        db.session.commit()

        print(body)  
        return Response(json.dumps(new_post.to_dict()), mimetype="application/json", status=201)
        
class PostDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
        

    def patch(self, id):
        # update post based on the data posted in the body 
        body = request.get_json()
        post = Post.query.filter(Post.id==id).first()
        if post == None or post.user.id != self.current_user.id:
            return Response(json.dumps({}), mimetype="application/json", status=404)

        post.image_url = body.get('image_url') or post.image_url
        post.caption = body.get('caption') or post.caption
        post.alt_text = body.get('alt_text') or post.alt_text

        db.session.commit()
        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)


    def delete(self, id):
        post = Post.query.filter(Post.id == id)
        

        if post.delete() == 0:
            return Response(json.dumps({}), mimetype="application/json", status=404)
                
        db.session.commit()
        return Response(json.dumps({}), mimetype="application/json", status=200)
        

    def get(self, id):
        # get the post based on the id
        posts = Post.query.filter(Post.id==id);
        try:
            post = [post.to_dict() for post in posts][0]

            if post.user_id not in get_authorized_user_ids(self.current_user.id):
                return Response(json.dumps({}), mimetype="application/json", status=404)    

            return Response(json.dumps(post), mimetype="application/json", status=200)
        except:
            return Response(json.dumps({}), mimetype="application/json", status=404)        
        

def initialize_routes(api):
    api.add_resource(
        PostListEndpoint, 
        '/api/posts', '/api/posts/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        PostDetailEndpoint, 
        '/api/posts/<int:id>', '/api/posts/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )