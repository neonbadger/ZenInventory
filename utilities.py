import os

def save_created_state(state):
    pass

def is_valid_state(state):
    return True

def make_authorization_url():
    """Serve a webpage on localhost that creates an authorization link
    out to clover.com"""

    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks

    from uuid import uuid4   
    state = str(uuid4())
    # save_created_state(state)
    
    params = {"client_id": os.environ['APP_ID'],
              "response_type": "code",
              "state": state,
              "redirect_uri": os.environ['REDIRECT_URI'],
              "duration": "temporary",
              "scope": "identity"}

    import urllib

    url = "https://www.clover.com/oauth/authorize?client_id" + os.environ['APP_ID'] + urllib.urlencode(params)
    return url

def get_token(code):

    params = {
        'client_id': os.environ['APP_ID'],
        'client_secret': os.environ['APP_SECRET'],
        'code': code
    }

    response = requests.post(
        "https://www.clover.com/oauth/token",
        data = params
    )

    token_json = response.json()
    access_token = token_json['access_token']

    return access_token

