import json
from flask import Flask, request

app = Flask(__name__)
post_id_counter = 2
comment_id_counter = 1
posts={
    0:{
        'id': 0,
        'score': 0,
        'text': "My First Post!",
        'username': "Young"
    
    },
    1:{
        'id': 1,
        'score': 0,
        'text': "My Second Post!",
        'username': "Young"

}
}
comments={
    0:[{
       'id': 0,
       'score': 0,
       'text': "My First Comment!",
       'username': "Young"
       }]

}


@app.route('/')
def root():
    """Default Rooting
    """
    return 'Hello world!'


@app.route('/api/posts/',methods=['GET'])
def get_posts():
    """Return lists of current posts
    """
    res={'success': True, 'data': list(posts.values())}
    return json.dumps(res),200


@app.route('/api/posts/', methods=['POST'])
def create_post():
    """Create a new post with input for 'text' and 'username' and return it
    """
    global post_id_counter
    req_data=json.loads(request.data)
    
    if 'text' in req_data and 'username' in req_data:
        post_body = {
            'text': req_data['text'],
            'username': req_data['username']
        }
        text=post_body['text']
        username=post_body['username']
  
        post = {
            'id': post_id_counter,
            'score': 0,
            'text': text,
            'username': username
        }
    
    elif 'text' not in req_data or 'username' not in req_data:
        return json.dumps({'success': False, 'error': 'User input not found!'}),404
    posts[post_id_counter]=post
    comments[post_id_counter]=[]
    post_id_counter += 1
    
    return json.dumps({'success': True, 'data': post}), 201


@app.route('/api/post/<int:post_id>/', methods=['GET'])
def get_post(post_id):
    """Return a post (post_id) 
    """
    if post_id in posts:
        post = posts[post_id]
        return json.dumps({'success': True, 'data': post}), 200
    
    return json.dumps({'success': False, 'error': 'Post not found!'}),404


@app.route('/api/post/<int:post_id>/', methods=['POST'])
def edit_post(post_id):
    """Save and return a post (post_id) with updated 'text' from user input 
    """
    if post_id in posts:
        req_data=json.loads(request.data)
        if 'text' not in req_data:
            return json.dumps({'success': False, 'error': 'User input not found!'}),404
        old_post=posts[post_id]
        old_post['text']=req_data['text']
        
        return json.dumps({'success': True, 'data': old_post}), 201
    
    return json.dumps({'success': False, 'error': 'Post not found!'}),404


@app.route('/api/post/<int:post_id>/',methods=['DELETE'])
def delete_post(post_id):
    """Delete the post (post_id) and return it
    """
    if post_id in posts:
        post=posts[post_id]
        del posts[post_id]
        
        return json.dumps({'success': True, 'data': post}), 200
    
    return json.dumps({'success': False, 'error': 'Post not found!'}),404


@app.route('/api/post/<int:post_id>/comments/',methods=['GET'])
def get_comments(post_id):
    """Return the list of current comments for the post (post_id) """
    if post_id in comments:
        comment=comments[post_id]
        res={'success': True, 'data': comment}
        
        return json.dumps(res),200
    
    return json.dumps({'success': False, 'error': 'Post not found!'}),404


@app.route('/api/post/<int:post_id>/comment/',methods=['POST'])
def post_comment(post_id):
    """Create and return a comment for the post (post_id) with 'text' 
    and 'username' from user input
    """
    global comment_id_counter
    if post_id in posts:
        req_data=json.loads(request.data)
        if 'text' not in req_data or 'username' not in req_data:
            return json.dumps({'success': False, 'error': 'User input not found!'}),404
    
        comment_body = {
            'text': req_data['text'],
            'username': req_data['username']
        }
        text=comment_body['text']
        username=comment_body['username']
        comment = {
            'id': comment_id_counter,
            'score': 0,
            'text': text,
            'username': username
        }
        comments[post_id].append(comment)
        comment_id_counter += 1
        
        return json.dumps({'success': True, 'data': comment}), 201
    
    return json.dumps({'success': False, 'error': 'Post not found!'}),404


@app.route('/api/post/<int:post_id>/comment/<int:comment_id>/',methods=['DELETE'])
def delete_comment(post_id, comment_id):
    """Delete and return the comment (comment_id) of the post (post_id)
    """
    if post_id in posts:
        for cmt in comments[post_id]:
            if 'id' in cmt and cmt['id']==comment_id:
                comment = cmt
                pos=comments[post_id].index(cmt)
                del comments[post_id][pos]
                return json.dumps({'success': True, 'data': comment}), 200



        """post=posts[post_id]
        del posts[post_id]
        
        return json.dumps({'success': True, 'data': post}), 200"""
    
    return json.dumps({'success': False, 'error': 'Comment not found!'}),404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
