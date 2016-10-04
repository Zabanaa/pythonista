from flask import jsonify
import functools
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
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        return_value = f(*args, **kwargs)
        status_code = None
        headers = None

        if isinstance(return_value, tuple): # The response is a tuple
            status_code, data, headers = return_value # unpack the tuple
            return_value = jsonify(data) # jsonify the response object
            return_value.status_code = status_code

            if headers is not None:
                return_value.headers.extend(headers)
        return return_value

    return wrapped

