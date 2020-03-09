import json
from flask import Flask, request
from db1 import db1, Post, Comment 


import sqlite3

app = Flask(__name__)
db1_filename = 'todo.db1'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db1_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db1.init_app(app)
with app.app_context():
    db1.create_all()


@app.route('/')
def root():
    """Default Rooting"""
    return 'Hello world!'

@app.route('/api/posts/',methods=['GET'])
def get_posts():
    """Return lists of current posts"""
    posts = Post.query.all()
    res={'success': True, 'data':[post.serialize() for post in posts]}
    return json.dumps(res),200

@app.route('/api/posts/', methods=['POST'])
def create_post():
    """Create a new post with input for 'text' and 'username' and return it
    """
    req_data=json.loads(request.data)
    post = Post(
        text = req_data.get('text'),
        username = req_data.get('username')
    )
    db1.session.add(post)
    db1.session.commit()
    return json.dumps({'success': True, 'data': post.serialize()}), 201

@app.route('/api/post/<int:post_id>/', methods=['GET'])
def get_post(post_id):
    """Return a post (post_id) """
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
         return json.dumps({'success': False, 'error': 'Post not found!'}),404
    return json.dumps({'success': True, 'data': post.serialize()}), 200

@app.route('/api/post/<int:post_id>/', methods=['POST'])
def edit_post(post_id):
    """Save and return a post (post_id) with updated 'text' from user input 
    """
    post = Post.query.filter_by(id=post_id).first()
    if post is not None:
        req_data=json.loads(request.data)
        post.text=req_data.get('text', post.text)
        post.username=req_data.get('username', post.username)
        db1.session.commit()
        return json.dumps({'success': True, 'data': post.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}),404

@app.route('/api/post/<int:post_id>/',methods=['DELETE'])
def delete_post(post_id):
    """Delete the post (post_id) and return it"""
    post = Post.query.filter_by(id=post_id).first()
    if post is not None:
        db1.session.delete(post)
        db1.session.commit()
        return json.dumps({'success': True, 'data': post.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}),404

@app.route('/api/post/<int:post_id>/comment/',methods=['POST'])
def create_comment(post_id):
    """Create a comment with the post (post_id) and return it"""
    post = Post.query.filter_by(id=post_id).first()
    if post is not None:
        req_data=json.loads(request.data)
        if 'text' in req_data and 'username' in req_data:
            comment =Comment(
                text = req_data.get('text'),
                username = req_data.get('username'),
                post_id = post.id
            )
            post.comments.append(comment)
            db1.session.add(comment)
            db1.session.commit()
            return json.dumps({'success': True, 'data': comment.serialize()}), 200
        
        return json.dumps({'success': False, 'error': 'User input not found!'}),404

    return json.dumps({'success': False, 'error': 'Post not found!'}),404

@app.route('/api/post/<int:post_id>/comments/', methods=['GET'])
def get_comments(post_id):
    """Return all the comments of a post (post_id) """
    post = Post.query.filter_by(id=post_id).first()
    if post is not None:
        comments = [comment.serialize() for comment in post.comments]
        return json.dumps({'success': True, 'data': comments}), 200
        
    return json.dumps({'success': False, 'error': 'Post not found!'}),404
    


# @app.route('/api/post/<int:post_id>/comments/',methods=['GET'])
# def get_comments(post_id):
#     """Return the list of current comments for the post (post_id) """
#     comment = db1.get_comment_by_id(post_id)
#     if comment is not None and db1.get_post_by_id(post_id) is not None:
#         res={'success': True, 'data': comment}
#         return json.dumps(res),200
#     return json.dumps({'success': False, 'error': 'Post not found!'}),404

# @app.route('/api/post/<int:post_id>/comment/',methods=['POST'])
# def post_comment(post_id):
#     """Create and return a comment for the post (post_id) with 'text' 
#     and 'username' from user input"""
#     req_data=json.loads(request.data)
#     if db1.get_post_by_id(post_id) is not None:
#         if 'text' in req_data and 'username' in req_data:
#             text=req_data['text']
#             username=req_data['username']
#             comments = {
#                 'id': db1.create_comment(text,username, post_id),
#                 'score': 0,
#                 'text': text,
#                 'username': username,
#                 'post_id': post_id
#             }
#             return json.dumps({'success': True, 'data': comments}), 201
#         return json.dumps({'success': False, 'error': 'User input not found!'}),404
#     return json.dumps({'success': False, 'error': 'Post not found!'}),404

"""@app.route('/api/post/<int:post_id>/comment/<int:comment_id>/',methods=['DELETE'])
def delete_comment(post_id, comment_id):
    Delete and return the comment (comment_id) of the post (post_id)
    
    if post_id in posts:
        for cmt in comments[post_id]:
            if 'id' in cmt and cmt['id']==comment_id:
                comment = cmt
                pos=comments[post_id].index(cmt)
                del comments[post_id][pos]
                return json.dumps({'success': True, 'data': comment}), 200

    return json.dumps({'success': False, 'error': 'Comment not found!'}),404"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
