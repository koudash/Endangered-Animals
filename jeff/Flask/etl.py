from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

title = "Fruits Database"
heading = "Fruits_DB"

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.fruits_db #Select the database
fruit = db.fruits #Select the collection name


#################################################
# Flask Routes
#################################################
def redirect_url():
    return request.args.get('next') or \
        request.referrer or \
        url_for('index')

@app.route("/")
def apis ():
    #Display the api paths
    return (
        f"Available Routes:<br/>"
        f"/api/banana<br/>"
        f"/api/peach"
    )

@app.route("/banana")
def yellow ():
    #Display only bananas
    bananas = fruit.find({"type":"banana"})
    a2="active"
    return render_template('index.html',a2=a2,fruit=bananas,t=title,h=heading)

@app.route("/peach")
def peachy ():
    #Display only peaches
    peaches = fruit.find({"type":"peach"})
    a3="active"
    return render_template('index.html',a3=a3,fruit=peaches,t=title,h=heading)


if __name__ == "__main__":
    app.run(debug=True)
