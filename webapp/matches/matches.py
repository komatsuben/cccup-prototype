from jinja2 import TemplateNotFound
import os
from db import db
from admin.models import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import PasswordField

from flask import Blueprint, render_template, abort, redirect, url_for, request, session, current_app, flash, jsonify
from jinja2 import TemplateNotFound

from .forms import MatchesForm

from datetime import datetime

from matches.models import Match

from db_connection import connection

import pytz, json


matches_bp = Blueprint(
    'matches_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/matches_bp',
)

COMPETITION_CHOICES = [
    "mini-soccer",
    "basket-putra",
    "basket-putri",
    "voli-putra",
    "voli-putri",
    "bulu-tangkis",
    "pencak-silat",
    "tenis-meja",
    "modern-dance",
    "band",
    "catur",
    "fotografi",
    "taekwondo",
    "english-debate",
    "short-movie",
    "wall-climbing",
    "cubing",
    "debat",
    "cerdas-cermat",
    "paduan-suara",
    "drama-modern",
    "digital-painting",
    "orasi",
]


def serialize_match(match):
    return {
        "id": match.id,
        "competition": match.competition,
        "team1": match.team1,
        "team2": match.team2,
        "team1_score": match.team1_score,
        "team2_score": match.team2_score,
        "status": match.status,
        "venue": match.venue,
        "stage": match.stage,
        "level": match.level,
        "streaming_link": match.streaming_link,
        "time": match.time.strftime("%d %b %Y %H:%M") if match.time else "",
        "last_updated": match.last_updated.strftime("%Y-%m-%d %H:%M:%S") if match.last_updated else "",
        "team1_set": match.team1_set,
        "team2_set": match.team2_set,
    }

@matches_bp.route('/dashboard')
def admin_home():
    return render_template('matches/dashboard.html')

@matches_bp.route('/')
def home():
    matches = Match.query.all()
    matches = [serialize_match(match) for match in matches]
    
    grouped_matches = {
        "Mini Soccer": {},
        "Basket Putra": {},
        "Basket Putri": {},
        "Voli Putra": {},
        "Voli Putri": {},
        "Bulu Tangkis": {},
        "Tenis Meja": {},
    }
    
    for match in matches:
        competition = match.get('competition')
        level = match.get("level")
        
        if competition in grouped_matches:
            if level not in grouped_matches[competition]:
                grouped_matches[competition][level] = []
            grouped_matches[competition][level].append(match)
    return render_template('matches/view_index.html', grouped_matches=grouped_matches)

@matches_bp.route('/match/<id>')
def view_match(id):
    # mongo_main = current_app.extensions["mongo_main"]
    # collection = mongo_main.db.matches
    
    # Fetch match details
    # match = collection.find_one({'_id': ObjectId(id)})
    # if not match:
    #     return "Match not found", 404
    
    # Serialize the match
    # match = serialize_document(match)
    
    # Extract competition type
    # competition = match.get('competition')

    # Render match page based on competition type
    # if competition == "Voli Putra" or competition == "Voli Putri":
    #     # Specific handling for Voli (with team set details)
    #     return render_template(
    #         'matches/view_voli.html', 
    #         match=match
    #     )
    
    # elif competition == "Bulu Tangkis" or competition == "Tenis Meja":
    #     # Specific handling for Bulutangkis (with multiple rounds)
    #     return render_template(
    #         'matches/view_bulutangkis.html', 
    #         match=match
    #     )
    
    # else:
    #     # Default match display for other competitions
    #     return render_template(
    #         'matches/view_match.html', 
    #         match=match
    #     )
    # delete later
    return render_template('matches/view_match.html')

@matches_bp.route('/add_match', methods=["GET", "POST"])
def add_match():
    # user = session.get('user', {})
    # if not user:
    #     return redirect(url_for('admin_bp.login'))
    
    
    form = MatchesForm()
    if form.validate_on_submit():
        team1_set_scores = []
        team2_set_scores = []
        
        for key in request.form.keys():
            if key.startswith('team1_set'):
                team1_set_scores.append(int(request.form[key]))
            elif key.startswith('team2_set'):
                team2_set_scores.append(int(request.form[key]))
        
        match = {
            "competition": form.competition.data,
            "team1": form.team1.data,
            "team2": form.team2.data,
            "team1_score": form.team1_score.data,
            "team2_score": form.team2_score.data,
            "status": form.status.data,
            "venue": form.venue.data,
            "stage": form.stage.data,
            "level": form.level.data,
            "streaming_link": form.streaming_link.data,
            # "time": form.time.data.strftime("%d %b %Y %H:%M"),
            # "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            # ISO FORMAT
            "time": form.time.data.strftime("%Y-%m-%d %H:%M:%S"),
            "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "team1_set": team1_set_scores,
            "team2_set": team2_set_scores,
        }
        INSERT_MATCH_QUERY = """
        INSERT INTO matches (
            competition, team1, team2, team1_score, team2_score, status, 
            venue, stage, level, streaming_link, time, last_updated, 
            team1_set, team2_set
            ) 
            VALUES (
                %(competition)s, %(team1)s, %(team2)s, %(team1_score)s, %(team2_score)s, %(status)s, 
                %(venue)s, %(stage)s, %(level)s, %(streaming_link)s, %(time)s, %(last_updated)s, 
                %(team1_set)s, %(team2_set)s
                ) RETURNING id;
            """
        try:
            cur = connection.cursor()
            cur.execute(INSERT_MATCH_QUERY, match)
            inserted_id = cur.fetchone()[0]
            connection.commit()
            cur.close()
            flash("Match added successfully", "success")
            return redirect(url_for('matches_bp.update_match', id=id.inserted_id))
        except Exception as e:
            connection.rollback()
            flash(f"Error adding match: {e}", "danger")
    return render_template('matches/add_match.html', form=form)

@matches_bp.route('/update_match/<id>', methods=["GET", "POST"])
def update_match(id):
    # user = session.get('user', {})
    # if not user:
    #     return redirect(url_for('admin_bp.login'))
    # mongo_main = current_app.extensions["mongo_main"]
    # collection = mongo_main.db.matches
    # match = collection.find_one({'_id': ObjectId(id)})
    # if match["competition"] in ["Bulu Tangkis", "Tenis Meja"]:
    #     return redirect(url_for("matches_bp.update_3_set_match", id=id))
    # form = MatchesForm(
    #     competition = match.get('competition', ''),
    #     team1 = match.get('team1', ''),
    #     team2 = match.get('team2', ''),
    #     status = match.get('status', ''),
    #     venue = match.get('venue', ''),
    #     stage = match.get('stage', ''),
    #     streaming_link = match.get('streaming_link', ''),
    #     level = match.get('level', ''),
    #     time = datetime.strptime(match.get('time', ''), "%d %b %Y %H:%M"),
    #     team1_score = match.get('team1_score', ''),
    #     team2_score = match.get('team2_score', ''),
    # )
    return render_template('matches/update_match.html')