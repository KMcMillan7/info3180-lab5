"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from flask import Blueprint, request, jsonify, current_app
from flask import render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from .forms import MovieForm
from .models import Movie, db
from flask_wtf.csrf import generate_csrf
from flask import send_from_directory

bp = Blueprint('app', __name__, url_prefix='/api/v1')


###
# Routing for your application.
###

@bp.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@bp.route('/movies', methods=['POST'])
def movies():
    form = MovieForm()
    if form.validate_on_submit():
        #Handle file upload
        file = form.poster.data
        filename = secure_filename(file.filename)

        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        #Save move to database
        movie = Movie(title=form.title.data, description=form.description.data, poster=filename)
        db.session.add(movie)
        db.session.commit()

        return jsonify({'message': 'Movie added successfully', 
                       'title': movie.title,
                       'poster': movie.poster,
                       'description': movie.description}), 201
    else:
        return jsonify({'errors': form_errors(form)}), 400
    
@bp.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.order_by(Movie.created_at.desc()).all()
    movies_list = []
    for movie in movies:
        movies_list.append({
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'poster': f'/api/v1/posters/{movie.poster}'
        })
    return jsonify({'movies': movies_list})

@bp.route('/csrf-token', methods=['GET'])
def get_csrf_token():
    return jsonify({'csrf_token': generate_csrf()})

@bp.route('/posters/<filename>')
def get_poster(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@bp.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return bp.send_static_file(file_dot_text)


@bp.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@bp.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404