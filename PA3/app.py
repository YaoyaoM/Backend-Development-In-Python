import json
from flask import Flask, request
from db import DB
import sqlite3

app = Flask(__name__)
db=DB()


@app.route('/')
def root():
    """Default Rooting"""
    return 'Hello world!'

@app.route('/api/posts/',methods=['GET'])
def get_posts():
    """Return lists of current posts"""
    res={'success': True, 'data': db.get_all_posts()}
    return json.dumps(res),200

@app.route('/api/posts/', methods=['POST'])
def create_post():
    """Create a new post with input for 'text' and 'username' and return it
    """
    req_data=json.loads(request.data)
    if 'text' in req_data and 'username' in req_data:
        post_body = {
            'text': req_data['text'],
            'username': req_data['username']
        }
        text=post_body['text']
        username=post_body['username']
        post = {
            'id': db.create_post(text,username),
            'score': 0,
            'text': text,
            'username': username
        }
    elif 'text' not in req_data or 'username' not in req_data:
        return json.dumps({'success': False, 'error': 'User input not found!'}),404
    return json.dumps({'success': True, 'data': post}), 201

@app.route('/api/post/<int:post_id>/', methods=['GET'])
def get_post(post_id):
    """Return a post (post_id) """
    post = db.get_post_by_id(post_id)
    if post is None:
         return json.dumps({'success': False, 'error': 'Post not found!'}),404
    return json.dumps({'success': True, 'data': post}), 200

@app.route('/api/post/<int:post_id>/', methods=['POST'])
def edit_post(post_id):
    """Save and return a post (post_id) with updated 'text' from user input 
    """
    if db.get_post_by_id(post_id) is not None:
        req_data=json.loads(request.data)
        if 'text' not in req_data:
            return json.dumps({'success': False, 'error': 'User input not found!'}),404
        text=req_data['text']
        post=db.edit_post_by_id(post_id, text)
        return json.dumps({'success': True, 'data': post}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}),404

@app.route('/api/post/<int:post_id>/',methods=['DELETE'])
def delete_post(post_id):
    """Delete the post (post_id) and return it"""
    if db.get_post_by_id(post_id) is not None:
        post=db.delete_post_by_id(post_id)
        return json.dumps({'success': True, 'data': post}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}),404

@app.route('/api/post/<int:post_id>/comments/',methods=['GET'])
def get_comments(post_id):
    """Return the list of current comments for the post (post_id) """
    comment = db.get_comment_by_id(post_id)
    if comment is not None and db.get_post_by_id(post_id) is not None:
        res={'success': True, 'data': comment}
        return json.dumps(res),200
    return json.dumps({'success': False, 'error': 'Post not found!'}),404

@app.route('/api/post/<int:post_id>/comment/',methods=['POST'])
def post_comment(post_id):
    """Create and return a comment for the post (post_id) with 'text' 
    and 'username' from user input"""
    req_data=json.loads(request.data)
    if db.get_post_by_id(post_id) is not None:
        if 'text' in req_data and 'username' in req_data:
            text=req_data['text']
            username=req_data['username']
            comments = {
                'id': db.create_comment(text,username, post_id),
                'score': 0,
                'text': text,
                'username': username,
                'post_id': post_id
            }
            return json.dumps({'success': True, 'data': comments}), 201
        return json.dumps({'success': False, 'error': 'User input not found!'}),404
    return json.dumps({'success': False, 'error': 'Post not found!'}),404

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
