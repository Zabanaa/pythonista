from app import db

class Company(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(100), nullable=False, unique=True)
    password    = db.Column(db.String(255), nullable=False)
    name        = db.Column(db.String(40), nullable=False)
    location    = db.Column(db.String(50), nullable=True)
    website     = db.Column(db.String(60), nullable=True)
    twitter     = db.Column(db.String(60), nullable=True)
    facebook    = db.Column(db.String(120), nullable=True)
    linkedin    = db.Column(db.String(180), nullable=True)
    bio         = db.Column(db.Text(), nullable=True)

    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)

    def serialise(self):
        return {
            "id"        : self.id,
            "email"     : self.email,
            "name"      : self.name,
            "location"  : self.location,
            "website"   : self.website,
            "twitter"   : self.twitter,
            "facebook"  : self.facebook,
            "linkedin"  : self.linkedin,
            "bio"       : self.bio
        }

    def __repr__(self):
        return "Company %s" % (self.name)
