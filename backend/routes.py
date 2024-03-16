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
        return jam['output']
    except:
        print("Failed to load json from response\n")
        print(response)
        return 0
    
@app.route('/regeneratemusic', methods=['POST'])
def regenerate_music():
    '''
    Generate a new sheet music in ABC notation using few shot prompt engineering with gpt 4
    '''
    data = request.get_json()
    response = regenerate_sheetmusic(data['chords'], data['scales'], data['title'], data['style'], data['example'])
    newjam = json.loads(response)
    print(newjam)
    return jsonify({"examplesong": newjam['output']})

if __name__ == '__main__':
    app.run(debug=True, port=8080)