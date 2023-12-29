#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import Flask, jsonify, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.orm import load_only
from forms import *
from models import db, Venue, Artist, Show


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  -------------------------------------------------------------------------#
#  Venues
#  -------------------------------------------------------------------------#


#  Create Venue 
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  error = False
  try:
      venue = Venue()
      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.address = form.address.data
      venue.phone = form.phone.data
      venue.website_link = form.website_link.data
      venue.genres = request.form.getlist('genres')
      venue.facebook_link = form.facebook_link.data
      venue.image_link = form.image_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data

      db.session.add(venue)
      db.session.commit()
  except:
      error = True
      db.session.rollback()
  finally:
      db.session.close()
      if error:
          flash('An error occured. Venue ' +
                  request.form['name'] + ' Could not be listed!')
      else:
          flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')

#  View All Venues
@app.route('/venues')
def venues():
 
  areas = Venue.query.with_entities(Venue.city, Venue.state).distinct(Venue.city, Venue.state).all()

  result = []
  for area in areas:
    city, state = area

    venues = Venue.query.filter(Venue.city == city, Venue.state == state).all()
    
    result_venues = []
    for venue in venues:
      result_venues.append({'id': venue.id, 'name': venue.name})

    result.append({'city': city, 'state': state, 'venues': result_venues})

  return render_template('pages/venues.html', areas=result)

#  Search Venue 
@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term')

  # Checks if the search term matches any of the Venues name, City or State
  venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%') | Venue.city.ilike(f"%{search_term}%") | Venue.state.ilike(f"%{search_term}%")).all()

  # Putting the results in a dict to capture the count and the data to populate the page
  results = {
    "count": len(venues),
    "data": [{'id': venue.id, 'name': venue.name } for venue in venues]
  }

  return render_template(
        "pages/search_venues.html",
        results=results,
        search_term=request.form.get("search_term", ""),
    )

#  View Venue
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)

    # Checks start time to differentiate between past and upcoming event 
    # Filters through and seperates them and storesin a variable 
    get_past_shows = list(filter(lambda x: x.start_time < datetime.today(), venue.shows))
    get_upcoming_shows = list(filter(lambda x: x.start_time >= datetime.today(), venue.shows))

    # Maps through past/upcoming shows and fills in the details of the show, including the venue image, hence calling the show_artist() func
    venue.past_shows = list(map(lambda x: x.show_artist(), get_past_shows))
    venue.upcoming_shows = list(map(lambda x: x.show_artist(), get_upcoming_shows))

    # Gets count to populate page
    venue.past_shows_count = len(venue.past_shows)
    venue.upcoming_shows_count = len(venue.upcoming_shows)

    # Formatting 
    venue.genres = venue.genres.replace('{', '').replace('}', '').split(',')

    return render_template('pages/show_venue.html', venue=venue)

#  Edit Venue 
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  # Pre populates fields so the user doesnt have to type everything again, they can just make edits
  venue = Venue.query.get(venue_id)
  form.name.data = venue.name
  venue.name = form.name.data
  form.city.data= venue.city 
  form.address.data = venue.address
  form.state.data   = venue.state 
  form.phone.data =   venue.phone 
  form.genres.data  =  venue.genres 
  form.facebook_link.data   = venue.facebook_link
  form.image_link.data  =  venue.image_link 
  form.website_link.data  =  venue.website_link 
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data  = venue.seeking_description

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm(request.form)

  try:
    venue = Venue.query.get(venue_id)

    # Replaces the orignal data with the updated form data
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.website_link = form.website_link.data
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = form.facebook_link.data
    venue.image_link = form.image_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data

    db.session.add(venue)
    db.session.commit()

    flash(request.form['name'] + ' was successfully updated!')

  except Exception as e:
    db.session.rollback()
    flash('An error occurred. ' + request.form['name'] + ' could not be updated.')

  finally:
    db.session.close()

  
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Delete Venue 
@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
    error = False
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        if error:
          flash('Venue could not be deleted. Please try again later')
        else:
          flash('Venue Succesfully deleted')
    return render_template('pages/home.html')


#  ------------------------------------------------------------------------#
#  Artists
#  ------------------------------------------------------------------------#
    
#  Create Artist
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  error = False
  try:
      artist = Artist()
      artist.name = form.name.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.genres = request.form.getlist('genres')
      artist.facebook_link = form.facebook_link.data
      artist.image_link = form.image_link.data
      artist.website_link = form.website_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data

      db.session.add(artist)
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      
      db.session.close()
      if error:
          flash('An error occured. Artist ' + request.form['name'] + ' Could not be listed!')
      else:
          flash('Artist ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')

#  View All Artists
@app.route('/artists')
def artists():
  artists = Artist.query.all()

  return render_template('pages/artists.html', artists=artists)

#  Search Artists
@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term')

  # Checks if the search term matches any of the Artists name, City or State
  artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%') | Artist.city.ilike(f"%{search_term}%") | Artist.state.ilike(f"%{search_term}%")).all()

  # Putting the results in a dict to capture the count and the data to populate the page
  results = {
    "count": len(artists),
    "data": [{'id': artist.id, 'name': artist.name } for artist in artists]
  }

  return render_template(
        "pages/search_artists.html",
        results=results,
        search_term=request.form.get("search_term", ""),
    )

#  View Artist
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)

    # Checks start time to differentiate between past and upcoming event 
    # Filters through and seperates them and storesin a variable 
    get_past_shows = list(filter(lambda x: x.start_time < datetime.today(), artist.shows))
    get_upcoming_shows = list(filter(lambda x: x.start_time >= datetime.today(), artist.shows))

    # Maps through past/upcoming shows and fills in the details of the show, including the venue image, hence calling the show_venue() func
    artist.past_shows = list(map(lambda x: x.show_venue(), get_past_shows))
    artist.upcoming_shows = list(map(lambda x: x.show_venue(), get_upcoming_shows))

    # Gets count to populate page
    artist.past_shows_count = len(artist.past_shows)
    artist.upcoming_shows_count = len(artist.upcoming_shows)

    # Formatting 
    artist.genres = artist.genres.replace('{', '').replace('}', '').split(',')

    return render_template('pages/show_artist.html', artist=artist)

#  Edit Artist 
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist = Artist.query.get(artist_id)

  # Pre populates fields so the user doesnt have to type everything again, they can just make edits
  form.name.data = artist.name
  artist.name = form.name.data
  form.city.data= artist.city 
  form.state.data   = artist.state 
  form.phone.data =   artist.phone 
  form.genres.data  =  artist.genres 
  form.facebook_link.data   = artist.facebook_link
  form.image_link.data  =  artist.image_link 
  form.website_link.data  =  artist.website_link 
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data  = artist.seeking_description

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm()
  try:

    artist = Artist.query.get(artist_id)

    # Replaces the orignal data with the updated form data
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.genres = request.form.getlist('genres')
    artist.facebook_link = form.facebook_link.data
    artist.image_link = form.image_link.data
    artist.website_link = form.website_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data

    db.session.commit()
    flash( request.form['name'] + ' was successfully updated!')

  except Exception as e:
    db.session.rollback()
    flash('An error occurred.' + request.form['name'] + ' could not be updated.')

  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

#  Delete Artist
@app.route('/artists/<artist_id>/delete', methods=['GET'])
def delete_artist(artist_id):
    error = False
    try:
        Artist.query.filter_by(id=artist_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        if error:
          flash('Artist could not be deleted. Please try again later')
        else:
          flash('Artist Succesfully deleted')
    return render_template('pages/home.html')



#  --------------------------------------------------------------------------#
#  Shows
#  --------------------------------------------------------------------------#

#  Create Show
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  error = False
  try:
      show = Show()
      show.artist_id= form.artist_id.data
      show.venue_id = form.venue_id.data
      show.start_time = request.form['start_time']

      db.session.add(show)
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
      if error:
          flash('An error occured. This show Could not be listed!')
      else:
          flash('This show was successfully listed!')

  return render_template('pages/home.html')

#  View All Shows
@app.route('/shows')
def shows():
  shows = Show.query.all()
  current_time = datetime.now()

  data = []

  for show in shows:
    artist = Artist.query.get(show.artist_id)
    venue = Venue.query.get(show.venue_id)

    if show.start_time > current_time:
      data.append({
          "venue_id": show.venue_id,
          "venue_name": venue.name,
          "artist_id": artist.id,
          "artist_name": artist.name,
          "artist_image_link": artist.image_link,
          "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
      })

  return render_template('pages/shows.html', shows=data)


#----------------------------------------------------------------------------#
# Errors
#----------------------------------------------------------------------------#

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

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
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
