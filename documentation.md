# When downloading the project you must first create a virtual env
# Then download all the dependencies (pip install -r requirements.txt)
# If you want to replicate my setup you can follow this tutotial (link to the digital
ocean article)
# You will also have to rename the config_example.py file , add your info and move it to
the pythonista package
# then all you have to do is sudo start pythonista, and the server should be running
# then visit whatever url your server is configured on and you should see the site
# To run the unittests just call python manage.py test
# To run the migrations you first need to initiate the process by calling 
python manage.py db init, then run the migrations by calling `python manage.py db migrate`
and finally to update everything just run `python manage.py db upgrade`

## here is what is left to do on the project

- Create a reset password functionality
- Create a front end using a framework of your choice
- Refactor the tests 
- Test email confirmation functionality 
- Decorate /api/confirm/token with ogin required
- Refactor serialise_json decorator
- Check that the company (user) is confirmed before letting them log in

## Here are all the authentication and api endpoints

## Other notes

All helper functions and methods are commented 
Tests are run using the unittest standard library (feel free to use the tool of your
choice)

## Next features to implement
- Profile images for companies
- Allow users to apply within the site
