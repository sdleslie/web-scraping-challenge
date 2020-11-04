# From last exercise in Web Scraping 3
# Flask App and Route
from flask import Flask, jsonify, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
# Add a new DB in Mongo DB in the Mongo IDE
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()
    
    # Return template and data
    return render_template("index.html", mars=destination_data)

@app.route("/scrape")
def scrape():

    # Run the scrape function
    marsdict = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, marsdict, upsert=True)

    return redirect("/")

# The dictionary gets stored in MongoDB

if __name__ == '__main__':
    app.run(debug=True,threaded=True)