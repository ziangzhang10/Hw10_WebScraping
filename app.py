# import flask
from flask import Flask, render_template, redirect

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# import the function that scrapes data from mars
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database.
db = client.mars_db

### NOTE: We technically could insert the data within this app.py file, but then we 
### would end up re-adding the data every time the server is loaded, unless we 
### dropped the data and reloaded in upon every server restart.

@app.route("/")
def index():
    # Fill in the info on the index with our mars dict
    pseudo_list = list(db.all_dict.find())
    return render_template("index.html", pseudo_list=pseudo_list)


@app.route("/scrape") 
def scraper():
    # scrape data
    all_dict = db.all_dict
    all_dict_data = scrape_mars.scrape()
    # update mongodb
    all_dict.update({}, all_dict_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
