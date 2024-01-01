"""
Artist, Venue and Show models
"""

# Imports
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))

    shows = db.relationship("Show", lazy=True, cascade="all, delete-orphan", backref="venues")

    def __repr__(self):
        return f'<Venue id:{self.id}> name:{self.name}>'


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))

    shows = db.relationship("Show", lazy=True, cascade="all, delete-orphan", backref="artists")

    def __repr__(self):
        return f'<Artist id:{self.id}> name:{self.name}>'


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id',  ondelete="CASCADE"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id', ondelete="CASCADE"),  nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    venue = db.relationship('Venue')
    artist = db.relationship('Artist')

    def __repr__(self):
      return f'<Show id:{self.id} venue_id:{self.venue_id} artist_id:{self.artist_id}>'
