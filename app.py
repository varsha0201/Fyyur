#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import ast
import babel
import json
import logging
import datetime
import traceback
import dateutil
import dateutil.parser
from dateutil.parser import parse
from dateutil.tz import gettz
from flask_script import Manager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_wtf import Form as BaseForm, FlaskForm
from flask_babel import Babel
from wtforms.validators import DataRequired
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY
from logging import Formatter, FileHandler
from babel.dates import format_date, format_datetime, format_time
from flask import abort, g, request
from forms import *
from models import *
from flask_migrate import Migrate
from models import db, Venue, Artist, Show
import models


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

babel = Babel(app)
app.config.from_object('config')
db = SQLAlchemy(app)
moment = Moment(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


def __init__(self, artist_id, venue_id,start_time):
      self.start_time=start_time
      self.venue_id=venue_id
      self.artist_id=artist_id
            
def insert(self):
      db.session.add(self)
      db.session.commit()



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

# TODO: replace with real venues data.
#       num_shows should be aggregated based on number of upcoming # shows per venue.

@app.route('/venues')
def venues():
    unique_city_states = Venue.query.distinct(Venue.city, Venue.state).all()
    data = [ucs.filter_on_city_state for ucs in unique_city_states]
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', None)
    venues = Venue.query.filter(
        Venue.name.ilike('%{}%'.format(search_term))).all()
        
    count_venues = len(venues)
    response = {
        "count": count_venues,
        "data": [v.serialize for v in venues]
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
# shows the venue page with the given venue_id
# TODO: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.filter(Venue.id == venue_id).one_or_none()
        
    if venue is None:
        abort(404)
  
    data = venue.serialize_with_shows_details
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    venue_form = VenueForm(request.form)

    try:
        new_venue = Venue(
            name=venue_form.name.data,
            genres=venue_form.genres.data,
            address=venue_form.address.data,
            city=venue_form.city.data,
            state=venue_form.state.data,
            phone=venue_form.phone.data,
            facebook_link=venue_form.facebook_link.data,
            image_link=venue_form.image_link.data)

        new_venue.add()
       
        flash('Venue ' +
              request.form['name'] +
              ' was successfully listed!')
    except Exception as ex:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
        traceback.print_exc()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue_to_delete = Venue.query.filter(search_venues.id == venue_id).one()
        venue_to_delete.delete()
        flash("Venue {0} has been deleted successfully".format(
            venue_to_delete[0]['name']))
    except NoResultFound:
        abort(404)


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    
    artists = Artist.query.all()
    data = [artist.serialize_with_shows_details for artist in artists]
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', None)
    artists = Artist.query.filter(
        Artist.name.ilike('%{}%'.format(search_term))).all()
    count_artists = len(artists)
    response = {
        "count": count_artists,
        "data": [a.serialize for a in artists]
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.filter(Artist.id == artist_id).one_or_none()
    

    if artist is None:
        abort(404)

    data = artist.serialize_with_shows_details
    

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist_form = ArtistForm()

    artist_to_update = Artist.query.filter(
        Artist.id == artist_id).one_or_none()
    
    if artist_to_update is None:
        abort(404)

    artist = artist_to_update.seriadmin@123
    
    form = ArtistForm(data=artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    try:
        artist = Artist.query.filter_by(id=artist_id).one()
        artist.name = form.name.data,
        artist.genres = form.genres.data,  
        artist.city = form.city.data,
        artist.state = form.state.data,
        artist.phone = form.phone.data,
        artist.facebook_link = form.facebook_link.data,
        artist.image_link = form.image_link.data,
        artist.update()
       
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except Exception as e:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be updated.')
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue_form = VenueForm()

    venue_to_update = Venue.query.filter(Venue.id == venue_id).one_or_none()
   
    if venue_to_update is None:
        abort(404)

    venue = venue_to_update.serialize
 
    form = VenueForm(data=venue)
 
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):  
    form = VenueForm(request.form)
    try:
        venue = Venue.query.filter(venue.id==venue_id).one()
        venue.name = form.name.data,
        venue.address = form.address.data,
        venue.genres = form.genres.data,  
        venue.city = form.city.data,
        venue.state = form.state.data,
        venue.phone = form.phone.data,
        venue.facebook_link = form.facebook_link.data,
        venue.image_link = form.image_link.data,
        venue.update()
        print(venue.name)
       
        
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except Exception as e:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be updated.')

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    artist_form = ArtistForm(request.form)

    try:
        new_artist = Artist(
            name=artist_form.name.data,
            genres=artist_form.genres.data,
            city=artist_form.city.data,
            state=artist_form.state.data,
            phone=artist_form.phone.data,
            facebook_link=artist_form.facebook_link.data,
            image_link=artist_form.image_link.data)

        new_artist.add()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as ex:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')

    return render_template('pages/home.html')



#  Shows
#  ----------------------------------------------------------------
# displays list of shows at /shows
# TODO: replace with real venues data.
#       num_shows should be aggregated based on number of upcoming shows per venue.


@app.route('/shows/create')
def create_shows():

  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    show_form = ShowForm(request.form)
    try:
        show = Show(
            artist_id=show_form.artist_id.data,
            venue_id=show_form.venue_id.data,
            start_time=show_form.start_time.data
        )
        show.add()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except Exception as e:
        flash('An error occurred. Show could not be listed.')

    return render_template('pages/home.html')

@app.route('/shows')
def shows():
      data = Show.query.with_entities(Show.start_time,Show.venue_id,
      Show.artist_id,Venue.name.label('venue_name'),Artist.name.label('artist_name'),
      Artist.image_link.label('artist_image_link')).join(Venue).join(Artist).all()
      return render_template('pages/shows.html', shows=data)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
0

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(host= '0.0.0.0')

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
