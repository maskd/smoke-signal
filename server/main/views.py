from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required, login_user
from werkzeug.exceptions import BadRequest

from server.main import methods
from server.login import LoginForm
from server.import_opml import create_db_from_opml

main = Blueprint("main", __name__,
                 template_folder="templates",
                 static_folder="static",
                 static_url_path="/main/static")


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        next_ = request.args.get("next")
        return redirect(next_ or url_for("main.index"))
    return render_template("login.html", form=form, error=form.error)


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        feeds = methods.get_all_feeds()
        return render_template('main.html', feeds=feeds)
    else:
        if "opml_file" not in request.files:
            raise BadRequest
        return methods.import_opml(request.files["opml_file"])


@main.route('/api/feed', methods=['GET', 'POST'])
@login_required
def all_feeds():
    if request.method == 'GET':
        return methods.get_all_feeds()
    if not request.is_json:
        raise BadRequest
    data = request.get_json()
    if "url" in data:
        return methods.post_feed(data["url"])
    elif "read" in data:
        return methods.mark_all_read()
    else:
        raise BadRequest


@main.route('/api/feed/<int:feed_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def feed(feed_id):
    if request.method == 'GET':
        page = request.args.get("page", 1, type=int)
        return methods.get_entries(page=page,
                                   feed_id=feed_id)
    elif request.method == 'POST':
        return methods.refresh_feed(feed_id)
    else:
        return methods.delete_feed(feed_id)


@main.route('/api/feed/<int:feed_id>/<predicate>', methods=['GET'])
@login_required
def all_feed_entries(feed_id, predicate):
    if predicate not in ["all", "read", "unread", "marked"]:
        raise BadRequest
    page = request.args.get("page", 1, type=int)
    return methods.get_entries(predicate=predicate, page=page,
                               feed_id=feed_id)


@main.route('/api/entry/<predicate>', methods=['GET'])
@login_required
def all_entries(predicate):
    if predicate not in ["all", "read", "unread", "marked"]:
        raise BadRequest
    page = request.args.get("page", 1, type=int)
    return methods.get_entries(predicate=predicate,
                               page=page)


@main.route('/api/entry/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def entry(entry_id):
    if request.method == 'GET':
        return methods.get_entry(entry_id)
    if not request.is_json:
        raise BadRequest
    data = request.get_json()
    if "read" in data or "marked" in data:
        return methods.toggle_status(entry_id,
                                     data)
    raise BadRequest
