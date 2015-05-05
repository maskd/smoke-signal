from smoke_signal import app
from flask import request, render_template
from smoke_signal.database.models import db, Feed, Entry
from smoke_signal.fetch_feed import read_feed
import json

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.route('/')
def show_feeds():
    feeds = db.session.query(Feed)
    return render_template('show_feeds.html', feeds=feeds)

@app.route('/feeds/<feed_id>')
def show_entries(feed_id):
    # feed_id is non-negative iff feed could be fetched
    if feed_id >= 0:
        feed = db.session.query(Feed).filter(Feed.id == feed_id).one()
        entries = db.session.query(Entry).filter(Entry.feed_id == feed_id).all()
    else:
        entries = []
    return json.dumps([e.serialize() for e in entries])

@app.route('/_refresh_entries/<feed_id>')
def refresh_entries(feed_id):
    feed = db.session.query(Feed).filter(Feed.id == feed_id).one()
    try:
        read_feed(feed)
    except:
        feed_id = -1
    return show_entries(feed_id)
