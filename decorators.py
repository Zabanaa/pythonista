from flask import jsonify
# Login required decorator
# check if company is in the session
# check that the session value is equal to the actual company name
# if so execute the function
# else return a 403 unauthorised and redirect the user


# Serialise Json

def serialise_json(f):
    '''

    Takes the object returned by the function called 
    and jsonifies it

    '''
    def wrapper():
        return_value = f()
        return_value = jsonify(return_value)
        return return_value

    return wrapper

