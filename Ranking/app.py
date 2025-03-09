from flask import Flask, request, jsonify
from utils.fetch_property import fetch_property
from utils.cache import get_cached_rank, set_cached_rank, invalidate_locality
from utils.rank import rank
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

@app.route('/')
def home():
    return "Hello, world!"


@app.route('/search', methods=['GET'])
def search_rooms():
    location = request.args.get('location')
    if not location:
        return jsonify({"error": "Missing 'location' parameter"}), 400

    try:
        data = fetch_property(f"http://localhost:8081/api/room/search?location={location}")
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/rank', methods=['GET'])
def ranked_rooms():
    location = request.args.get('query')
    if not location:
        return jsonify({"error": "Missing 'location' parameter"}), 400

    # Check cache first
    cached_data = get_cached_rank(location)
    if cached_data is not None:
        return jsonify({"source": "cache", "data": cached_data})

    try:
        data = fetch_property(f"http://localhost:8081/api/room/query?query={location}")
        ranked_data = rank(data)

        set_cached_rank(location, ranked_data)

        return jsonify(ranked_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
from flask import Flask, request, jsonify

@app.route('/invalidate-cache', methods=['POST'])
def invalidate_cache():
    location = request.args.get('location')
    if not location:
        return jsonify({"error": "Missing 'location' parameter"}), 400

    invalidate_locality(location)

    return jsonify({"message": f"Cache invalidated for location: {location}"}), 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)