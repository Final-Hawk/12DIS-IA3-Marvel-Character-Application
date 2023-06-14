from flask import Flask, render_template, request
import requests
import time
import hashlib
# Import config file to get the API keys and proxy settings
from config import PUBLIC_KEY, PRIVATE_KEY, PROXY_CONFIG, PROXY_NEEDED

app = Flask(__name__)

# Base URL for the Marvel API
API_URL = "http://gateway.marvel.com/v1/public/"

# Check if proxy is needed and set the proxies accordingly
if PROXY_NEEDED:
    proxies = PROXY_CONFIG
else:
    proxies = {}


def generateAuth():
    # Generate authentication parameters for the Marvel API request.
    timestamp = str(time.time())
    hash_string = timestamp + PRIVATE_KEY + PUBLIC_KEY
    hash = hashlib.md5(hash_string.encode('utf-8')).hexdigest()
    return {'ts': timestamp, 'apikey': PUBLIC_KEY, 'hash': hash, 'limit': 100}


@app.route('/')
def index():
    # Render the index page.
    # If a search query is provided, call the search function with the query.
    # Otherwise, call the showAll function to display all characters.
    query = request.args.get('search')
    if query:
        return search(query)
    else:
        return showAll()


def showAll():
    # Fetch and display all characters from the Marvel API.
    url = API_URL + "characters"
    # Make the request to the Marvel API with the authentication parameters
    response = requests.get(url, proxies=proxies, params=generateAuth())
    # Parse the JSON response and store the required data in a list
    data = response.json()
    characters = []
    for character in data['data']['results']:
        # Get the character ID, name, description, number of comics and stories
        characterID = character['id']
        name = character['name']
        if character['description'] == "" or character['description'] == " ":
            description = "No description available."
        else:
            description = character['description']
        numcomics = character['comics']['available']
        numstories = character['stories']['available']
        thumbnaildata = character['thumbnail']
        thumbnail = thumbnaildata['path'] + '.' + thumbnaildata['extension']
        # Check if the character has a thumbnail image
        if 'image_not_available' not in thumbnail:
            # Append the character data to the list
            characters.append({'characterID': characterID,
                               'name': name,
                               'description': description,
                               'thumbnail': thumbnail,
                               'numcomics': numcomics,
                               'numstories': numstories})
    return render_template('index.html', characters=characters)


@app.route("/character/<id>")
def character(id):
    # Fetch and display individual character information from the Marvel API.
    # Args: id (str): Character ID.
    url = API_URL + "characters/" + id
    response = requests.get(url, proxies=proxies, params=generateAuth())
    data = response.json()
    characterIndividual = []
    for character in data['data']['results']:
        # Get the character name, description, number of comics and stories
        name = character['name']
        if character['description'] == "" or character['description'] == " ":
            description = "No description available."
        else:
            description = character['description']
        numcomics = character['comics']['available']
        numstories = character['stories']['available']
        thumbnaildata = character['thumbnail']
        thumbnail = thumbnaildata['path'] + '.' + thumbnaildata['extension']

        if 'image_not_available' not in thumbnail:
            # Append the character data to the list
            characterIndividual.append({'name': name,
                                        'description': description,
                                        'thumbnail': thumbnail,
                                        'numcomics': numcomics,
                                        'numstories': numstories})

    # Get the comics associated with the character
    characterComics = []
    for comic in data['data']['results'][0]['comics']['items']:
        name = comic['name']
        characterComics.append({'name': name})

    # Get the stories associated with the character
    characterStories = []
    for story in data['data']['results'][0]['stories']['items']:
        name = story['name']
        characterStories.append({'name': name})
    # Render the index page with the character data
    return render_template('indexIndividual.html',
                           characters=characterIndividual,
                           comics=characterComics,
                           stories=characterStories)


def search(query):
    # Display characters matching the provided query from the Marvel API.
    # Args: query (str): Search query.
    url = API_URL + "characters?nameStartsWith=" + query
    # Make the request to the Marvel API with the authentication parameters
    response = requests.get(url, proxies=proxies, params=generateAuth())
    data = response.json()
    characters = []
    for character in data['data']['results']:
        # Get the character ID, name, description, number of comics and stories
        characterID = character['id']
        name = character['name']
        if character['description'] == "" or character['description'] == " ":
            description = "No description available."
        else:
            description = character['description']
        numcomics = character['comics']['available']
        numstories = character['stories']['available']
        thumbnaildata = character['thumbnail']
        thumbnail = thumbnaildata['path'] + '.' + thumbnaildata['extension']

        if 'image_not_available' not in thumbnail:
            # Append the character data to the list
            characters.append({'characterID': characterID,
                               'name': name,
                               'description': description,
                               'thumbnail': thumbnail,
                               'numcomics': numcomics,
                               'numstories': numstories})
    # Render the index page with the search results
    return render_template('index.html', characters=characters, query=query)


if __name__ == '__main__':
    # Run the app on localhost:5000
    app.run(debug=False)
