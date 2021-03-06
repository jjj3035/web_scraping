# import necessary libraries
import os
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/rest";

app = Flask(__name__)

app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    mars_new_data = scrape_mars.scrape()
    mars_data.update(
        {},
        mars_new_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)