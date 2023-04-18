from flask import Response, request
from flask_restful import Resource
from models import Bookmark, Post, db
import json

class BookmarksListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # get all bookmarks owned by the current user
        bookmarks = Bookmark.query.filter(Bookmark.user_id==self.current_user.id);
        return Response(json.dumps([bookmark.to_dict() for bookmark in bookmarks]), mimetype="application/json", status=200)

    def post(self):
        # create a new "bookmark" based on the data posted in the body 
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

        bookmark = Bookmark(self.current_user.id, body.get('post_id'))
        
        try:
            db.session.add(bookmark)
            db.session.commit()
            return Response(json.dumps(bookmark.to_dict()), mimetype="application/json", status=201)
        except:
            return Response(json.dumps({}), mimetype="application/json", status=400)

class BookmarkDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):

        
        bookmark = Bookmark.query.filter(Post.id == id)
        

        if bookmark.delete() == 0:
            return Response(json.dumps({}), mimetype="application/json", status=404)
                
        db.session.commit()
        return Response(json.dumps({}), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<int:id>', 
        '/api/bookmarks/<int:id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
