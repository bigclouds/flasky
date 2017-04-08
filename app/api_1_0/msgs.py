from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Post, Permission
from . import api
from .decorators import permission_required
from .errors import forbidden


@api.route('/msgs/')
def get_msgs():
    page = request.args.get('page', 1, type=int)
    pagination = Msg.query.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    msgs = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_msgs', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_msgs', page=page+1, _external=True)
    return jsonify({
        'posts': [msg.to_json() for msg in msgs],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/msgs/<int:id>')
def get_msg(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/msgs/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_new():
    post = Msg.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('api.get_post', id=post.id, _external=True)}


@api.route('/msgs/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_msg(id):
    msg = Msg.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permissions')
    msg.body = request.json.get('body', msg.body)
    db.session.add(msg)
    return jsonify(msg.to_json())
