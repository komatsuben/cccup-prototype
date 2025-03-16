from db import db

class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    competition = db.Column(db.String(255), nullable=False)
    team1 = db.Column(db.String(255), nullable=False)
    team2 = db.Column(db.String(255), nullable=False)
    team1_score = db.Column(db.Integer, nullable=False)
    team2_score = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    venue = db.Column(db.String(255), nullable=False)
    stage = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    streaming_link = db.Column(db.Text)
    time = db.Column(db.DateTime, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False)
    team1_set = db.Column(db.JSON, nullable=False)
    team2_set = db.Column(db.JSON, nullable=False)
