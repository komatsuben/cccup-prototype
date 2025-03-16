from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, FieldList, FormField, DateTimeLocalField
from wtforms.validators import URL, DataRequired

class SetScoreForm(FlaskForm):
    class Meta:
        csrf = False
    score = IntegerField('Score', default=0)

class MatchesForm(FlaskForm):
    team1 = StringField('Team 1', validators=[DataRequired()])
    team2 = StringField('Team 2', validators=[DataRequired()])
    status = SelectField('Status', choices=[("Scheduled", "Scheduled"), ("Live", "Live"), ("Done", "Done")], validators=[DataRequired()])
    venue = SelectField('Venue', choices=[("Sportshall", "Sportshall"), ("Lapangan Voli", "Lapangan Voli"), ("Lapangan Basket", "Lapangan Basket"),("Lapangan Minisoccer", "Lapangan Minisoccer")], validators=[DataRequired()])
    stage = SelectField('Stage', choices=[("Final", "Final"), ("Semifinal", "Semifinal"), ("Quarterfinal", "Quarterfinal"), ("Qualifier","Qualifier")])
    competition = SelectField('Competition', choices=[("Mini Soccer", "Mini Soccer"), ("Basket Putra", "Basket Putra"), ("Basket Putri", "Basket Putri"), ("Voli Putra", "Voli Putra"), ("Voli Putri", "Voli Putri"), ("Pencak Silat", "Pencak Silat"), ("Modern Dance", "Modern Dance"), ("Band", "Band"), ("Catur", "Catur"), ("Fotografi", "Fotografi"), ("Taekwondo", "Taekwondo"), ("English Debate", "English Debate"), ("Short Movie", "Short Movie"), ("Wall Climbing", "Wall Climbing"), ("Cubing", "Cubing"), ("Debat", "Debat"), ("Cerdas Cermat", "Cerdas Cermat"), ("Paduan Suara", "Paduan Suara"), ("Drama Modern", "Drama Modern"), ("Digital Painting", "Digital Painting"), ("Orasi", "Orasi") ])
    time = DateTimeLocalField('Match Schedule', format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    level = SelectField('Level', choices=[("SMP", "SMP"),("SMA", "SMA")])
    streaming_link = StringField('Streaming Link (must use https://)')
    current_time = StringField("current_time")
    team1_score = IntegerField('Team 1 Score', default=0)
    team2_score = IntegerField('Team 2 Score', default=0)
    
    team1_set = FieldList(FormField(SetScoreForm), min_entries=0)
    team2_set = FieldList(FormField(SetScoreForm), min_entries=0)