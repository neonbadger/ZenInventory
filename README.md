**ZenInventory: For Your Business's Peace of Mind**

####ABOUT

ZenInventory is a simple Flask web app that allows a merchant to view inventory via the Clover API.

The goal is to explore Clover's OAUTH 2.0 and endpoints. 

####INSTALLATION

To install ZenInventory on your local machine:

Clone this repo.

```
$ git clone https://github.com/neonbadger/DestinationUnknown.git
```

Create a virtual environment for the project.

```
$ virtualenv env
```
Apply for a developer account from [Clover](https://www.clover.com/developers/).

Store the APP_ID, APP_SECRET, REDIRECT_URI, and MERCHANT_ID in a shell script and source it.

```
$ source secrets.sh
```
Run the app on your local machine. The default port is 5000.
```
$ python main.py
```
####TO-DO

- [ ] Dynamic Routing for Individual Inventory Item
- [ ] Update inventory from the app
- [ ] Visualize the item stocks
- [ ] Testing