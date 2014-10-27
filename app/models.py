from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    videotron_username = db.Column(db.String(64), index=True, unique=True)
    bandwidth_allowed = db.Column(db.Integer, index=True, unique=False)
    bandwidth_used = db.Column(db.Integer, index=True, unique=False)
    timestamp = db.Column(db.DateTime, unique=False)

    def __repr__(self):
        return '<videotron User %r>' % self.videotron_username