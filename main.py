"""
ZenInventory: A Web App that Helps Merchants View their Clover Inventory

Complete:
(1) Clover OAuth 2.0
(2) Explore Clover's REST API endpoints
(3) MVP

To do:
(1) Render individual routing with dynamic URL routing
(2) Build database
(3) POST methods to update inventory
"""

from flask import Flask, abort, request, redirect, render_template, flash, session
import os
import clover_api
from utilities import save_created_state, is_valid_state, make_authorization_url, get_token



app = Flask(__name__)
app.secret_key = os.urandom(24)



@app.route('/')
def homepage():
    """Homepage that directs users to Clover for authorization"""

    auth_url = make_authorization_url()

    return render_template('homepage.html', 
                            auth_url=auth_url)



@app.route('/clover_callback')
def clover_callback():
    """Clover OAuth 2.0 handshake to exchange code for access token"""
   
    error = request.args.get('error', '')

    if error:
        return "Error: " + error

    state = request.args.get('state', '')

    if not is_valid_state(state):
        abort(403)

    code = request.args.get('code')
    access_token = get_token(code)

    session['access_token'] = access_token

    return redirect('/inventory')


@app.route('/show_token')
def show_token():
    """Test route to check if access token is fresh"""

    return "Access token is %s" % session['access_token']


@app.route('/inventory')
def inventory_list():
    """Show inventory"""

    c = clover_api.CloverAPI(session['access_token'], os.environ['MERCHANT_ID'])

    response = c.get("/v3/merchants/{}/items".format(os.environ['MERCHANT_ID']))
    stock = c.get("/v3/merchants/{}/item_stocks".format(os.environ['MERCHANT_ID']))

    items = response['elements']

    print items
    print stock

    for item in items:
        print item['name'], item['price'], item['id']

    ### Note to self: write the returned object into a database and query ###

    return render_template("all_orders.html", items=items)

@app.route("/item/<int:item_id>")
def show_order(item_id):
    """Show inventory details"""

    ### UNDER CONSTRUCTION ###

    c = clover_api.CloverAPI(session['access_token'], os.environ[MERCHANT_ID])

    response = c.get("/v3/merchants/{}/items".format(os.environ[MERCHANT_ID]))

    order = response['elements'][item_id]

    return render_template("order_detail.html", order=order)


if __name__ == '__main__':
    app.run(debug=True)
