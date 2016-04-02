# ZenInventory: For Your Business's Peace of Mind #

####ABOUT
![](/static/img/cover.png)

**ZenInventory** is a simple Flask web app that allows a merchant to view inventory via the Clover API.

The goal is to explore Clover's OAUTH 2.0 and API endpoints. 

Suggestions are welcome!

####INSTALLATION

To install ZenInventory on your local machine:

Clone this repo.

```
$ git clone https://github.com/neonbadger/ZenInventory.git
```

Create a virtual environment for the project.

```
$ virtualenv env
```
Install dependencies.
```
$ pip install -r requirements.txt
```

Apply for a developer account from [Clover](https://www.clover.com/developers/).

Store the APP_ID, APP_SECRET, REDIRECT_URI, and MERCHANT_ID in a shell script (i.e. secrets.sh)and source it.

```
$ source secrets.sh
```
Run the app on your local machine. The default port is 5000.
```
$ python main.py
```
####TO-DO

- [ ] Dynamic routing for individual inventory item
- [ ] Update inventory from the app
- [ ] Visualize item stocks
- [ ] Testing