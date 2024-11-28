# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Hardcoded configuration
PORT = 5000
OPENAI_API_KEY = "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"  # Replace with your actual OpenAI API key
IMAGE_API_KEY = "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"  # Optional, if using image generation

# Initialize OpenAI with the API key
openai.api_key = OPENAI_API_KEY

# Example Image Generation API endpoint (optional)
IMAGE_GEN_API_URL = "https://api.imagegen.example.com/generate"

@app.route('/api/player-info', methods=['POST'])
def get_player_info():
    data = request.get_json()
    logging.debug(f'Received Data: {data}')  # For debugging
    person_name = data.get('name', '').strip()

    if not person_name:
        logging.error('Person name is missing.')
        return jsonify({'message': 'Person name is missing.'}), 400

    try:
        # Check if the person is a well-known public figure
        verification_prompt = (
            f"Is {person_name} a well-known public figure, such as a celebrity, politician, athlete, etc.? Answer with 'Yes' or 'No'."
        )

        logging.debug(f'GPT-4 Verification Prompt: {verification_prompt}')

        verification_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a knowledgeable assistant."},
                {"role": "user", "content": verification_prompt}
            ],
            max_tokens=10,
            temperature=0
        )

        verification_text = verification_response['choices'][0]['message']['content'].strip().lower()
        logging.debug(f'Verification Response: {verification_text}')

        if verification_text != 'yes':
            return jsonify({'message': "Sorry, don't know him/her."}), 200

        # Generate biography using OpenAI's GPT-4 via ChatCompletion API
        biography_prompt = (
            f"Provide a concise and informative biography for {person_name}. "
            "The biography should include key details such as early life, career highlights, achievements, "
            "notable works, influence, and personal life. Present the information in clear and distinct bullet points."
        )

        logging.debug(f'GPT-4 Biography Prompt: {biography_prompt}')

        response = openai.ChatCompletion.create(
            model="gpt-4",  # Ensure you have access to GPT-4 or use "gpt-3.5-turbo" as an alternative
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": biography_prompt}
            ],
            max_tokens=500,
            temperature=0.7,
        )

        biography_text = response['choices'][0]['message']['content'].strip()
        # Split the biography into bullet points
        biography = [point.strip() for point in biography_text.split('\n') if point.strip()]

        logging.debug(f'Generated Biography: {biography}')

        # Optional: Generate person image using an image generation API
        # Uncomment and configure the following block if you wish to implement image generation
        """
        import requests

        image_headers = {
            'Authorization': f'Bearer {IMAGE_API_KEY}',
            'Content-Type': 'application/json'
        }
        image_payload = {
            'prompt': f'An artistic image of {person_name}'
        }
        image_response = requests.post(IMAGE_GEN_API_URL, json=image_payload, headers=image_headers)

        if image_response.status_code == 200:
            image_data = image_response.json()
            image_url = image_data.get('url')
        else:
            logging.error('Failed to generate image.')
            image_url = None
        """

        # If skipping image generation, set image_url to None or a placeholder
        image_url = None  # Replace with actual image URL if using image generation

        return jsonify({'biography': biography, 'imageUrl': image_url}), 200

    except openai.error.OpenAIError as e:
        logging.error(f'OpenAI API Error: {str(e)}')
        return jsonify({'message': 'Error generating biography.'}), 500
    except Exception as e:
        logging.error(f'Error: {str(e)}')
        return jsonify({'message': 'Error fetching person information.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
