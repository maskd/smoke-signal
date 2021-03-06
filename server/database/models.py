import sqlalchemy as sql
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from time import mktime

Base = declarative_base()


class Entry(Base):
    __tablename__ = "entry"

    id = sql.Column(sql.Integer, primary_key=True)
    title = sql.Column(sql.String, nullable=False)
    guid = sql.Column(sql.String, nullable=False)
    text = sql.Column(sql.String, nullable=False)
    url = sql.Column(sql.String, nullable=False)
    read = sql.Column(sql.Boolean, nullable=False)
    marked = sql.Column(sql.Boolean, nullable=False)
    pub_date = sql.Column(sql.DateTime, nullable=False)
    feed_id = sql.Column(sql.Integer, sql.ForeignKey('feed.id'))

    def __init__(self, title, guid, url, text, feed_id, pub_date=None):
        self.title = title
        self.guid = guid
        self.text = text
        self.url = url
        self.read = False
        self.marked = False
        if pub_date is None:
            self.pub_date = datetime.fromtimestamp(0)
        else:
            self.pub_date = datetime.fromtimestamp(mktime(pub_date))
        self.feed_id = feed_id

    def __unicode__(self):
        return '<title {}, text {}>'.format(self.title, self.text)

    def serialize(self):
        href = "/feeds/{}/{}".format(self.feed_id, self.id)
        links = {
            "self": {
                "href": href
            }
        }
        return {'title': self.title, 'text': self.text,
                'url': self.url, 'id': self.id,
                'feed_id': self.feed_id, 'read': self.read,
                'marked': self.marked, '_links': links,
                'pub_date': self.pub_date.isoformat()}


class Feed(Base):
    __tablename__ = "feed"

    id = sql.Column(sql.Integer, primary_key=True)
    title = sql.Column(sql.String, nullable=False)
    url = sql.Column(sql.String, nullable=False)
    entries = relationship('Entry', backref='feed', lazy='dynamic')
    unread = column_property(
        sql.select([sql.func.count(Entry.read) -
                    sql.func.sum(sql.cast(Entry.read, sql.Integer))]).
        where(Entry.feed_id == id).
        correlate_except(Entry)
    )

    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __unicode__(self):
        return '<title {}, url {}>'.format(self.title, self.url)

    def serialize(self):
        href = "/feeds/{}".format(self.id)
        links = {
            "self": {"href": href},
            "find": {
                "href": "{}{{?id}}".format(href),
                "templated": True
            }
        }
        return {'id': self.id, 'title': self.title, 'url': self.url,
                '_links': links,
                'unread': getattr(self, 'unread')}


class User(Base):
    __tablename__ = "user"

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String, nullable=False)
    password = sql.Column(sql.String, nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.name)
