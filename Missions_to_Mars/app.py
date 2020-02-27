from flask import Flask, render_template
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_data


@app.route("/scrape")
def scrape():
    data = scrape_mars.scrape()
    db.mars_data.insert_one(data)

@app.route('/')
def pass_data():
    data = (db.mars_data.find())
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)