from flask import Blueprint, request
from .helpers import *
from ..decorators import serialise_json, login_required

api = Blueprint('api', __name__, template_folder="pages")

@api.route('/confim/<token>', methods=['GET'])
def confirm_registration(token):
    return confirm_email(token)


@api.route('/companies', methods=['GET'])
@serialise_json
def companies():
    return get_companies()

@api.route('/companies', methods=['POST'])
@serialise_json
def register():
    form = request.get_json()
    return register_company(form)

@api.route('/companies/<int:company_id>', methods=['GET'])
@serialise_json
def company(company_id):
    return get_company(company_id)

@api.route('/companies/<int:company_id>', methods=['PUT'])
@serialise_json
@login_required
def modify_company(company_id):
    form = request.get_json()
    return update_company(company_id, form)

@api.route('/companies/<int:company_id>/jobs', methods=['GET'])
@serialise_json
def company_jobs(company_id):
    return get_company_jobs(company_id)

@api.route('/jobs', methods=['POST'])
@serialise_json
@login_required
def post_job():
    form = request.get_json()
    return publish_job(form)

@api.route('/jobs', methods=['GET'])
@serialise_json
def jobs():
    return get_jobs()

@api.route('/jobs/<int:job_id>', methods=['GET'])
@serialise_json
def job(job_id):
    return get_job(job_id)

@api.route('/jobs/<int:job_id>', methods=['PUT'])
@serialise_json
@login_required
def edit_job(job_id):
    form = request.get_json()
    return update_job(job_id, form)

@api.route('/jobs/<int:job_id>', methods=['DELETE'])
@serialise_json
@login_required
def delete_job(job_id):
    return remove_job(job_id)


@api.route('/jobs/<string:contract_type>', methods=['GET'])
@serialise_json
def job_type(contract_type):
    return get_job_type(contract_type)
