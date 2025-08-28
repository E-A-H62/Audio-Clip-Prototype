# Import required libraries
from flask import Flask, render_template, jsonify  # Flask web framework components
import requests  # HTTP library for making API calls
import os  # Operating system interface for environment variables
from dotenv import load_dotenv  # Load environment variables from .env file

# Load environment variables from .env file
load_dotenv()

# Get API Gateway URL from environment variable for security
API_GATEWAY_URL = os.getenv('API_GATEWAY_URL')

# Validate that the required environment variable is set
if not API_GATEWAY_URL:
    raise ValueError("API_GATEWAY_URL environment variable is not set. Please check your .env file.")

# Initialize Flask application
app = Flask(__name__)

@app.route('/')
def index():
    """Main route - serves the audio segmentation interface"""
    return render_template('segment_selection.html')

@app.route('/audio/<track_id>', methods=['GET'])
def get_audio_url(track_id):
    """
    API endpoint to fetch audio URL for a given track ID
    Makes a request to the external API Gateway and returns the signed URL
    """
    try:
        print(f"Requesting audio URL for Track ID: {track_id}")

        # Make HTTP request to the API Gateway to get the audio URL
        response = requests.get(f"{API_GATEWAY_URL}/tracks/{track_id}")
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse the JSON response from the API Gateway
        response_data = response.json()
        preview_url = response_data.get('preview_url', None)  # Extract the preview URL

        # Validate that we received a valid URL
        if preview_url:
            print(f"Preview URL received: {preview_url}")
            return jsonify({"signed_url": preview_url}), 200  # Return success with URL
        else:
            print("Error: No audio URL returned or invalid file type")
            return jsonify({"error": "Invalid or unsupported audio file"}), 415  # 415 Unsupported Media Type

    except requests.exceptions.RequestException as e:
        # Handle network/HTTP errors
        print(f"Request failed: {e}")
        return jsonify({"error": str(e)}), 500  # Return 500 Internal Server Error


if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True)  # Enable debug mode for development
