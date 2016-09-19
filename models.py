from app import db

class Company(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(100), nullable=False, unique=True)
    password    = db.Column(db.String(32), nullable=False)
    name        = db.Column(db.String(40), nullable=False, unique=True)
    location    = db.Column(db.String(50), nullable=True)
    website     = db.Column(db.String(60), nullable=True)
    twitter     = db.Column(db.String(60), nullable=True)
    facebook    = db.Column(db.String(120), nullable=True)
    linkedin    = db.Column(db.String(180), nullable=True)
    bio         = db.Column(db.Text(), nullable=True)

    def __init__(self, email, password, name, location, website, twitter, facebook, linkedin, bio):
        self.email      = email
        self.password   = password
        self.name       = name
        self.location   = location
        self.website    = website
        self.twitter    = twitter
        self.facebook   = facebook
        self.linkedin   = linkedin
        self.bio        = bio

    def __repr__(self):
       return "Company %s" % (self.name)
