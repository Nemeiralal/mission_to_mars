import sys
from flask import Flask, render_template, jsonify, redirect
#import pymongo
import scrape_sites_for_mars
from flask_pymongo import pymongo

sys.setrecursionlimit(3000)
app = Flask(__name__)


client = pymongo.MongoClient()
database = client['mars_data']
collection = database.mars_facts



@app.route('/scrape')
def scrape():
    mars_Scrapping_Result = scrape_sites_for_mars.scrape()
    database.mars_facts.insert_one(mars_Scrapping_Result)
    return"""<html>
	<center>
    <h2>Data and images are fetched through scrapping</h2>
    <p align="Center">
        <a class="btn btn-primary btn-lg" href="/" role="button">Show Scrapped Data</a>
    </p>
	</center>
    </html>
    """

@app.route("/")
def home():
    mars_data_from_DB = list(database.mars_facts.find())
    print(mars_data_from_DB)
    return render_template("myindex.html",  mars_data = mars_data_from_DB)


if __name__ == "__main__":
    app.run(debug=True)