"""
Artist, Venue and Show models
"""

# Imports
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))

    shows = db.relationship("Show", backref="venues", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Venue id:{self.id}> name:{self.name}>'


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))

    shows = db.relationship("Show", backref="artists", lazy=True)

    def __repr__(self):
        return f'<Artist id:{self.id}> name:{self.name}>'


class Show(db.Model):
    __tablename__ = 'shows'

    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)

    venue = db.relationship('Venue')
    artist = db.relationship('Artist')

    def __repr__(self):
      return f'<Show id:{self.id} venue_id:{self.venue_id} artist_id:{self.artist_id}>'