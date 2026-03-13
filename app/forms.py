# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message="Title is required"), Length(min=1, max=255, message="Title must be between 1 and 255 characters")])
    description = TextAreaField('Description', validators=[DataRequired(message="Description is required")])
    poster = FileField('Poster', validators=[
        FileRequired(message="Poster image is required"),
        FileAllowed(['jpg','jpeg', 'png', 'gif'], 'Images only!')
    ])