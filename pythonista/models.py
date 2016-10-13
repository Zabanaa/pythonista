from . import db
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
    confirmed   = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if key == 'password':
                value = self.hash_password(value)
            setattr(self, key, value)

    def get_url(self):
        return url_for('api.company', company_id=self.id)

    def get_jobs(self):
        return url_for('api.company_jobs', company_id=self.id, _external=True)

    def hash_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def serialise(self):
        return {
            "id"            : self.id,
            "bio"           : self.bio,
            "email"         : self.email,
            "name"          : self.name,
            "location"      : self.location,
            "website"       : self.website,
            "twitter"       : self.twitter,
            "facebook"      : self.facebook,
            "linkedin"      : self.linkedin,
            "total_staff"   : self.total_staff,
            "company_url"   : self.get_url(),
            "jobs_url"      : self.get_jobs()
        }

    def __repr__(self):
        return "Company %s" % (self.name)

class Job(db.Model):

    CONTRACTS = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract',  'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote')
    ]

    id                  = db.Column(db.Integer, primary_key=True)
    tags                = db.Column(db.String(255), nullable=False)
    title               = db.Column(db.String(70), nullable=False)
    description         = db.Column(db.Text(), nullable=False)
    salary_range        = db.Column(db.String(60), nullable=True)
    salary_max          = db.Column(db.String(10), nullable=True)
    salary_min          = db.Column(db.String(10), nullable=True)
    contract_type       = db.Column(ChoiceType(CONTRACTS), nullable=False)
    company_id          = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    def __init__(self, properties):
        for key, value in properties.items():
            setattr(self, key, value)

    def get_url(self):
        return url_for("api.job", job_id=self.id, _external=True)

    def get_company(self):
        return url_for("api.company", company_id=self.company_id, _external=True)

    def serialise(self):
        return {
            "id"        : self.id,
            "tags"      : self.tags,
            "title"     : self.title,
            "description"   : self.description,
            "salary_range"  : "%s - %s" % (self.salary_min, self.salary_max),
            "contract_type" : self.contract_type.value,
            "company": self.get_company(),
            "url": self.get_url()
        }

    def __repr__(self):
        return self.title
