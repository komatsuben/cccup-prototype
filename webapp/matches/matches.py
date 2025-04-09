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
    user = session.get('user', {})
    if not user:
        return redirect(url_for('admin_bp.login'))
    
    matches = Match.query.all()
    matches = [serialize_match(match) for match in matches]
    
    grouped_matches = {}

    ongoing_grouped_matches = {}  # Grouping ongoing matches by competition

    today = datetime.now().date()  # Get today's date

    for match in matches:
        competition = match.get('competition')
        level = match.get("level")
        match_time = datetime.strptime(match.get('time'), "%d %b %Y %H:%M")  # Convert to datetime
        
        if competition not in grouped_matches:
            grouped_matches[competition] = {}

        # Group ongoing matches by competition
        if match_time.date() == today:
            if competition not in ongoing_grouped_matches:
                ongoing_grouped_matches[competition] = []
            ongoing_grouped_matches[competition].append(match)

        # Group all matches
        if competition in grouped_matches:
            if level not in grouped_matches[competition]:
                grouped_matches[competition][level] = []
            grouped_matches[competition][level].append(match)

    return render_template(
        'matches/dashboard.html',
        grouped_matches=grouped_matches,
        ongoing_grouped_matches=ongoing_grouped_matches,  # Pass grouped ongoing matches
    )

@matches_bp.route('/') 
def home():
    matches = Match.query.all()
    matches = [serialize_match(match) for match in matches]
    
    grouped_matches = {}

    ongoing_grouped_matches = {}  # Grouping ongoing matches by competition

    today = datetime.now().date()  # Get today's date

    for match in matches:
        competition = match.get('competition')
        level = match.get("level")
        match_time = datetime.strptime(match.get('time'), "%d %b %Y %H:%M")  # Convert to datetime
        
        if competition not in grouped_matches:
            grouped_matches[competition] = {}

        # Group ongoing matches by competition
        if match_time.date() == today:
            if competition not in ongoing_grouped_matches:
                ongoing_grouped_matches[competition] = []
            ongoing_grouped_matches[competition].append(match)

        # Group all matches
        if competition in grouped_matches:
            if level not in grouped_matches[competition]:
                grouped_matches[competition][level] = []
            grouped_matches[competition][level].append(match)

    return render_template(
        'matches/view_index.html',
        grouped_matches=grouped_matches,
        ongoing_grouped_matches=ongoing_grouped_matches,  # Pass grouped ongoing matches
    )

@matches_bp.route('/match/<id>') 
def view_match(id):
    try:
        cur = connection.cursor()
        SELECT_MATCH_QUERY = "SELECT * FROM matches WHERE id = %s;"
        cur.execute(SELECT_MATCH_QUERY, (id,))
        row = cur.fetchone()
        cur.close()

        if not row:
            return "Match not found", 404

        # Define column names based on the database schema
        columns = ["id", "competition", "team1", "team2", "team1_score", "team2_score", "status",
                    "venue", "stage", "level", "streaming_link", "time", "last_updated", "team1_set",
                    "team2_set"]
        
        # Convert row into a dictionary
        match = dict(zip(columns, row))
        
        # Convert datetime to string for rendering if necessary
        if isinstance(match["time"], datetime):
            # match["time"] = match["time"].strftime('%Y-%m-%d %H:%M:%S')
            match["time"] = match["time"].strftime('%A, %d %B %Y %H:%M:%S')
        
        competition = match.get("competition")

        # Render template based on competition type
        if competition in ["Voli Putra", "Voli Putri"]:
            return render_template('matches/view_voli.html', match=match)
        elif competition in ["Bulu Tangkis", "Tenis Meja"]:
            return render_template('matches/view_bulutangkis.html', match=match)
        else:
            return render_template('matches/view_match.html', match=match)
    
    except Exception as e:
        return f"Error fetching match: {e}", 500
    
@matches_bp.route('/add_match', methods=["GET", "POST"])
def add_match():
    form = MatchesForm()
    
    if form.validate_on_submit():
        team1_set_scores = []
        team2_set_scores = []
        
        for key in request.form.keys():
            if key.startswith('team1_set'):
                team1_set_scores.append(int(request.form[key]))
            elif key.startswith('team2_set'):
                team2_set_scores.append(int(request.form[key]))
        
        new_match = Match(
            competition=form.competition.data,
            team1=form.team1.data,
            team2=form.team2.data,
            team1_score=form.team1_score.data,
            team2_score=form.team2_score.data,
            status=form.status.data,
            venue=form.venue.data,
            stage=form.stage.data,
            level=form.level.data,
            streaming_link=form.streaming_link.data,
            time=form.time.data,  # Assuming it's already a datetime object
            last_updated=datetime.utcnow(),
            team1_set=team1_set_scores,
            team2_set=team2_set_scores
        )

        try:
            db.session.add(new_match)
            db.session.commit()
            flash("Match added successfully", "success")
            return redirect(url_for('matches_bp.update_match', id=new_match.id))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding match: {e}", "danger")
    return render_template('matches/add_match.html', form=form)

@matches_bp.route('/update_match/<int:id>', methods=['GET', 'POST'])
def update_match(id):
    # Fetch match record using SQLAlchemy
    match_record = Match.query.get(id)

    if not match_record:
        flash("Match not found.", "danger")
        return redirect(url_for('matches_bp.add_match'))

    # Create form and prefill data
    form = MatchesForm(obj=match_record)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if request.method == "GET":
        form.team1_set.entries.clear()
        form.team2_set.entries.clear()
        
        for score in match_record.team1_set or []:
            form.team1_set.append_entry({"score": score})

        for score in match_record.team2_set or []:
            form.team2_set.append_entry({"score": score})
    
    if form.validate_on_submit():
        # Update match fields from form data
        form.populate_obj(match_record)
        match_record.last_updated = datetime.now()

        try:
            db.session.commit()
            flash("Match updated successfully", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating match: {e}", "danger")

    return render_template('matches/update_match.html', form=form, match_id=id, current_time=current_time)


@matches_bp.route('/remove_match/<id>', methods=['POST', 'GET'])
def remove_match(id):
    # user = session.get('user', {})
    # if not user:
    #     return redirect(url_for('admin_bp.login'))
    
    match = Match.query.get(id)
    if match:
        try:
            db.session.delete(match)
            db.session.commit()
            flash("Match has been deleted", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleting match: {e}", "danger")
    else:
        flash("Match not found.", "danger")
    return redirect(url_for('matches_bp.admin_home'))