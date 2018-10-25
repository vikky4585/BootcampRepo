from flask import Flask, jsonify,render_template,redirect
import mission_to_mars as mm
import pymongo


app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db_name = 'mars_db'
db = client[db_name]
db_details = db['details']

@app.route('/scrape')
def scrape():
    data = mm.scrape()
    db_details.insert(data)
    return redirect("/", code=302)

@app.route('/')
def home():
    
    fetchData = db_details.find().limit(1).sort('$natural', pymongo.DESCENDING)
    #fetchData = db_details.find()
    print(f'Rendering scrapped data {fetchData}')
    return render_template('index.html', scraped=fetchData)
    

if __name__ == "__main__":
    app.run(debug=True)
