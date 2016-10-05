from app import db
from flask import url_for
from sqlalchemy_utils.types.choice import ChoiceType
from werkzeug.security import check_password_hash, generate_password_hash

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
    instagram   = db.Column(db.String(120), nullable=True)
    bio         = db.Column(db.Text(), nullable=True)
    total_staff = db.Column(db.Integer, nullable=True)
    total_jobs  = db.relationship('Job', backref='company', lazy='dynamic')

    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if key == 'password':
                value = self.hash_password(value)
            setattr(self, key, value)

    def get_url(self):
        return url_for('company', company_id=self.id, _external=True)

    #def get_jobs(self):
    #    return url_for('app.get_company_jobs', company_id=self.id, _external=True)

    def hash_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def serialise(self):
        return {
            "id"        : self.id,
            "bio"       : self.bio,
            "email"     : self.email,
            "name"      : self.name,
            "location"  : self.location,
            "website"   : self.website,
            "twitter"   : self.twitter,
            "facebook"  : self.facebook,
            "linkedin"  : self.linkedin,
            "total_staff": self.total_staff,
            "resource_url": self.get_url()
    #        "jobs"      : self.get_jobs()
        }

    def __repr__(self):
        return "Company %s" % (self.name)

class Job(db.Model):

    CONTRACTS = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract',  'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote')
    ]

    id                  = db.Column(db.Integer, primary_key=True)
    tags                = db.Column(db.String(255), nullable=False)
    title               = db.Column(db.String(70), nullable=False)
    description         = db.Column(db.Text(), nullable=False)
    salary_range        = db.Column(db.String(60), nullable=True)
    contract_type       = db.Column(ChoiceType(CONTRACTS), nullable=False)
    company_id          = db.Column(db.Integer, db.ForeignKey('company.id'))

    def __init__(self, **properties):
        for key, value in properties.items():
            setattr(self, key, value)

    def get_url(self):
        return url_for("app.get_job_by_id", job_id=self.id, _extract=True)


    def serialise(self):
        return {
            "id"        : self.id,
            "tags"      : self.tags,
            "title"     : self.title,
            "description"   : self.description,
            "salary_range"  : self.salary_range,
            "contract_type" : self.contract_type,
            "company_id"    : self.company_id
        }

    def __repr__(self):
        return self.title





