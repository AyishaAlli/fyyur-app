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


#  ----------------------------------------------------------------
#  Venues
#  ----------------------------------------------------------------


#  Create Venue 
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  try:
      venue = Venue()
      venue.name = request.form['name']
      venue.city = request.form['city']
      venue.state = request.form['state']
      venue.address = request.form['address']
      venue.phone = request.form['phone']
      all_genres = request.form.getlist('genres')
      venue.genres = ','.join(all_genres)
      venue.facebook_link = request.form['facebook_link']

      if request.form['seeking_talent'] == 'y':
        venue.seeking_talent = True
      elif request.form['seeking_talent'] == 'n':
        venue.seeking_talent = False

      db.session.add(venue)
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
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
  locations =  Venue.query.with_entities(Venue.city, Venue.state).distinct(Venue.state).all()

  result = []
  for location in locations:
    city, state = location

    venues = Venue.query.filter(Venue.city == city, Venue.state == state).all()
    
    result_venues = []
    for venue in venues:
      result_venues.append({'id': venue.id, 'name': venue.name})

    result.append({'city': city, 'state': state, 'venues': result_venues})

  return render_template('pages/venues.html', areas=result)

#  Search Venue 
@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_query = request.form.get("search_term", "")

  search_response = {"count": 0, "data": []}

  fields = ["id", "name"]
  venue_search_results = (
    db.session.query(Venue)
    .filter(Venue.name.ilike(f"%{search_query}%"))
    .options(load_only(*fields))
    .all()
  )

  search_response["count"] = len(venue_search_results)

  for result in venue_search_results:
        item = {
            "id": result.id,
            "name": result.name,
        }
        search_response["data"].append(item)

  return render_template(
        "pages/search_venues.html",
        results=search_response,
        search_term=request.form.get("search_term", ""),
    )

#  View Venue
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)

    get_past_shows = list(filter(lambda x: x.start_time < datetime.today(), venue.shows))
    get_upcoming_shows = list(filter(lambda x: x.start_time >= datetime.today(), venue.shows))
    past_shows = list(map(lambda x: x.show_artist(), get_past_shows))
    upcoming_shows = list(map(lambda x: x.show_artist(), get_upcoming_shows))

    
    venue.past_shows = past_shows
    venue.upcoming_shows = upcoming_shows
    venue.past_shows_count = len(past_shows)
    venue.upcoming_shows_count = len(upcoming_shows)

    return render_template('pages/show_venue.html', venue=venue)

#  Edit Venue (get & post)
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))


#  Delete Venue 
# NOT WORKING YET!!!!!
@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exe_info())
    finally:
        db.session.close()
        return jsonify({ 'success': True })


#  ----------------------------------------------------------------
#  Artists
#  ----------------------------------------------------------------
    
#  Create Artist
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  try:
      artist = Artist()
      artist.name = request.form['name']
      artist.city = request.form['city']
      artist.state = request.form['state']
      artist.phone = request.form['phone']
      all_genres = request.form.getlist('genres')
      
      artist.facebook_link = request.form['facebook_link']
      artist.image_link = request.form['image_link']
      artist.website_link = request.form['website_link']

      artist.seeking_description = request.form['seeking_description']

      if request.form['seeking_venue'] == 'y':
         artist.seeking_venue = True

      genres = []
      for genre in all_genres:
         genres.append(genre)

      artist.genres = genres
      
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
  search_query = request.form.get("search_term", "")

  search_response = {"count": 0, "data": []}

  fields = ["id", "name"]
  artist_search_results = (
    db.session.query(Artist)
    .filter(Artist.name.ilike(f"%{search_query}%"))
    .options(load_only(*fields))
    .all()
  )

  search_response["count"] = len(artist_search_results)

  for result in artist_search_results:
        item = {
            "id": result.id,
            "name": result.name,
        }
        search_response["data"].append(item)

  return render_template(
        "pages/search_venues.html",
        results=search_response,
        search_term=request.form.get("search_term", ""),
    )

#  View Artist
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)

    genres = []
    for genre in artist.genres:
        genres.append(genre)

    get_past_shows = list(filter(lambda x: x.start_time < datetime.today(), artist.shows))
    get_upcoming_shows = list(filter(lambda x: x.start_time >= datetime.today(), artist.shows))
    past_shows = list(map(lambda x: x.show_artist(), get_past_shows))
    upcoming_shows = list(map(lambda x: x.show_artist(), get_upcoming_shows))

    artist.genres = genres
    artist.past_shows = past_shows
    artist.upcoming_shows = upcoming_shows
    artist.past_shows_count = len(past_shows)
    artist.upcoming_shows_count = len(upcoming_shows)

    return render_template('pages/show_artist.html', artist=artist)

  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  # return render_template('pages/show_artist.html', artist=data)

#  Edit Artist (get & post)
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))



#  ----------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------

#  Create Show
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  try:
      show = Show()
      show.artist_id= request.form['artist_id']
      show.venue_id = request.form['venue_id']
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


#  NOT COMPLETE
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

  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  return render_template('pages/shows.html', shows=data)





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
