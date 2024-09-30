from flask import Flask, jsonify, request
import wikipediaapi
import requests
import os

app = Flask(__name__)

# Initialize Wikipedia API with a custom User-Agent
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent="CelebrityInfoApp/1.0 (https://yourappurl.com/; contact@yourapp.com)"
)

# Root route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Celebrity Info API! Use the '/celebrity' endpoint to get information."})

# Helper function to get the Wikipedia page summary
def get_celebrity_description(name):
    page = wiki_wiki.page(name)
    if page.exists():
        summary = page.summary[:500]  # Get first 500 characters from the summary
        return summary
    return None

# Helper function to get the Wikipedia image link
def get_celebrity_image(name):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'thumbnail' in data and 'source' in data['thumbnail']:
            return data['thumbnail']['source']
    return None

@app.route('/celebrity', methods=['GET'])
def get_celebrity_info():
    # Extract celebrity name from the request
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Please provide a celebrity name'}), 400
    
    # Get the celebrity description
    description = get_celebrity_description(name)
    if not description:
        return jsonify({'error': 'Celebrity not found on Wikipedia'}), 404
    
    # Get the celebrity image link
    image_url = get_celebrity_image(name)
    if not image_url:
        image_url = 'No image available'

    # Return the result as JSON
    return jsonify({
        'name': name,
        'description': description,
        'image_url': image_url
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
