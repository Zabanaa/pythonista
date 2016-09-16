Pythonista API structure 

ROUTES 
-----------------------------

## Accounts x Users
/login                    
/logout                  
/register               

## Jobs 
/ AND /jobs            
/jobs/full-time       
/jobs/part-time      
/jobs/contract      
/jobs/intership    
/jobs/new         
/jobs/id AND /jobs/title        
/jobs/id/edit/                 

## Companies 
/companies 
/companies/id AND /companies/name
/companies/name/jobs AND /companies/id/jobs

## Optional

How to handle the updating of users profiles


API
------------------------------
/api/jobs/                               GET x POST
/api/jobs/id/                            GET x PUT x DELETE
/api/companies/                          GET x POST
/api/companies/id/                       GET x PUT
/api/companies/id/jobs/                  GET 


MODELS
----------------------------------

## Users
    - username
    - password
    - email
    - id
    - last_login_time (later on)
    - company_id (one to one field)

## Jobs
    - id (PK)
    - Name
    - tags
    - description
    - salary_range
    - type
    - company_id (Foreign Key)
    - user_id (Foreign Key)

## Companies (user profile)
    - ID (PK x AUTO INCREMENT)
    - Name (unique)
    - founded_on
    - city
    - total_staff
    - URL 
    - bio
    - address
    - twitter
    - fb
    - instagram
    - linkedin
    - total_jobs
    - logo
    - user_id (one to one field)

Should jobs be associated with users or company profiles or both ?

## Templates 

- login.html
- register.html
- jobs.html (will contain FT/PT/Contract/Intership/Remote)
- jobs__new.html (will POST to /api/jobs)
- jobs__detail.html
- jobs__edit.html (will POST to /api/jobs/id)
- companies__edit.html 
- companies__detail.html
- companies__jobs.html


## Additonal Notes 

POST to /api/jobs/

pass in the type of job
then filter by type when calling a specific endpoint 
ex: when the user hits /jobs/full-time, fetch jobs from the db that correspond to that
type


POST to /api/jobs/id
