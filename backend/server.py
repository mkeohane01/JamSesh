from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import generate_jam_from_gpt, regenerate_sheetmusic
import json

app = Flask(__name__)
CORS(app)

@app.route('/generatejam', methods=['POST'])
def generate_gpt():
    '''
    Generate response using few shot prompt engineering with gpt 4
    '''
    data = request.get_json()
    print(data)
    prompt = data.get('input')
    response = generate_jam_from_gpt(prompt)
    try:
        jam = json.loads(response)
        print(jam['output'])
        return jsonify(jam['output']), 200
    except Exception as e:
        print(f"Failed to load json from response\n {e}")
        print(response)
        return jsonify({"error": e}), 500
    
@app.route('/regeneratemusic', methods=['POST'])
def regenerate_music():
    '''
    Generate a new sheet music in ABC notation using few shot prompt engineering with gpt 4
    '''
    data = request.get_json()
    response = regenerate_sheetmusic(data['chords'], data['scales'], data['title'], data['style'], data['example'])
    try:
        newjam = json.loads(response)
        return jsonify({"examplesong": newjam['output']}), 200
    except Exception as e:
        print(f"Failed to load json from response\n {e}")
        print(response)
        return jsonify({"error": e}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)