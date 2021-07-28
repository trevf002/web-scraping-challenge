from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost:27017/mars_db"
mongo=PyMongo(app)

@app.route("/")
def index():
  data=mongo.db.mars.find_one()
  return render_template("index.html", mars=data)

@app.route("/scraping")
def scrap():
  #data=mongo.db.mars
  data = scraping.scrape_all()
  #mars=scrape_mars.scrape()
  #data.update({}, mars, upsert=True)
  mongo.db.mars.update({}, data, upsert=True)
  return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
