"""
ZenInventory: A Web App that Helps Merchants View their Inventory
"""

from flask import Flask, abort, request, redirect, render_template, flash
import os
import clover_api
from urlparse import urlparse

# import json
# import jsonify

from flask import session

import requests
import requests.auth

app = Flask(__name__)
app.requests_session = requests.Session()

app.secret_key = os.urandom(24)


# APP_ID = "PPY2CD6SA86FY"
# APP_SECRET = "4065d73d-ef74-937b-6ac5-d9982540348f"
# MERCHANT_ID = "W96Q5MJDPAN4P"
# REDIRECT_URI = "http://localhost:5000/clover_callback"
# BASE_URL = "https://www.clover.com"


@app.route('/')
def homepage():

    # text = '<a href="%s">Authenticate with Clover</a>'
    # return text % make_authorization_url()
    auth_url = make_authorization_url()
    # print auth_url

    return render_template('homepage.html', 
                            auth_url=auth_url)


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

def save_created_state(state):
    pass

def is_valid_state(state):
    return True

def get_token(code):

    parameters = {
        'redirect_uri': os.environ['REDIRECT_URI'],
        'code': code,
        'grant_type': 'authorization_code',
    }

    response = requests.post(
        "https://www.clover.com/oauth/token",
        auth = {
            os.environ['APP_ID'],
            os.environ['APP_SECRET']
        },
        data = parameters
    )

    return response


    # client_auth = requests.auth.HTTPBasicAuth(APP_ID, APP_SECRET)
    # post_data = {"grant_type": "authorization_code",
    #              "code": code,
    #              "redirect_uri": REDIRECT_URI}
    # response = requests.get("https://www.clover.com/oauth/token",
    #                          auth=client_auth,
    #                          data=post_data)
    # print response
    # return response

# def get_redirect_uri(request):
#     """Return OAuth redirect URI."""
#     parsed_url = urlparse(request.url)
#     if parsed_url.hostname == 'localhost':
#         return 'http://{hostname}:{port}/submit'.format(
#             hostname=parsed_url.hostname, port=parsed_url.port
#         )
#     return 'https://{hostname}/submit'.format(hostname=parsed_url.hostname)

@app.route('/clover_callback')
def clover_callback():
   
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        abort(403)

    code = request.args.get('code')


    # post_data = {
    #     'redirect_uri': REDIRECT_URI,
    #     'code': code,
    #     'grant_type': 'authorization_code',
    # }

    params = {
        'client_id': os.environ['APP_ID'],
        'client_secret': os.environ['APP_SECRET'],
        'code': code
    }

    response = requests.post(
        "https://www.clover.com/oauth/token",
        # auth = {
        #     APP_ID,
        #     APP_SECRET,
        #     code
        # },
        # data = post_data
        data = {
            'client_id': os.environ['APP_ID'],
            'client_secret': os.environ['APP_SECRET'],
            'code': code
        }
    )

    token_json = response.json()
    access_token = token_json['access_token']

    session['access_token'] = access_token

    # return "got an access token! %s" % access_token
    return redirect('/orders')


@app.route('/show_token')
def show_token():

    return "Access token is %s" % session['access_token']



@app.route('/orders')
def orders():

    c = clover_api.CloverAPI(session['access_token'], os.environ['MERCHANT_ID'])

    response = c.get("/v3/merchants/{}/items".format(os.environ['MERCHANT_ID']))

    orders = response['elements']

    for order in orders:
        print order['name'], order['price'], order['id']


    # # return 'success'

    # print session['access_token']
    # access_token = session['access_token']

    # headers = {"Authorization": "bearer " + access_token}

    # response = requests.get("https://api.clover.com/v3/merchants/{}/orders".format(MERCHANT_ID), headers=headers)
    # print "response", response
    # # print json.dump(data)

    # return 'success'

    return render_template("all_orders.html", orders=orders)

@app.route("/order/<int:order_id>")
def show_order(order_id):

#     return render_template("order_details.html",
#                             order=order)

    c = clover_api.CloverAPI(session['access_token'], MERCHANT_ID)

    response = c.get("/v3/merchants/{}/items".format(MERCHANT_ID))

    order = response['elements'][str(order_id)]

    return "order %s" % order


if __name__ == '__main__':
    app.run(debug=True)
