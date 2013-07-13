from flask import Flask
from flask import render_template
from flask import jsonify
import simplejson as json
import rdio
import urllib2

app = Flask(__name__)

TUMBLR_CONSUMER_KEY = "tumblr_consumer_key"
CONSUMER_KEY = "consumer_key"
SECRET_KEY = "secret_key"

r = rdio.Api(CONSUMER_KEY, SECRET_KEY)
app.debug = True

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/party")
def party():
    return render_template('party.html')  

@app.route('/rdio')
def rdio():
    return "Soon."

@app.route('/soundcloud')
def soundcloud():
    return render_template('soundcloud.html')

@app.route('/spotify')
def spotify():
    return "Very soon."

@app.route("/search/<trackname>")
def search(trackname):
    #Make ajax search and data return
    data = r.search(query=trackname, types=["Track"])
    return jsonify({'tracks': [{"name": track.name, "key": track.key, "artist": track.artist_name} for track in data.results]})

@app.route("/getgifs")
def gifs():
    tags = ['gif'] #Normally I use more than just gif but you can use any tags
    import random
    tag = random.choice(tags)
    response = urllib2.urlopen("http://api.tumblr.com/v2/tagged?tag="+tag+"&api_key="+ TUMBLR_CONSUMER_KEY)    
    body = json.loads(response.read())
    gifs = [gif['photos'][0]['original_size'] for gif in body['response'] if gif['type'] == 'photo']
    body = {"data" : gifs}
    return jsonify(**body)

if __name__ == "__main__":
    app.run()
