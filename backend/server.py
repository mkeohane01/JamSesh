from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt_utils import generate_jam_from_gpt, regenerate_sheetmusic, generate_harmony_from_jam, get_chord_abc 
import json

app = Flask(__name__)
CORS(app)

@app.route('/generatejam', methods=['POST'])
def generate_gpt():
    '''
    Generate response using few shot prompt engineering with gpt 4
    '''
    data = request.get_json()
    # print(data)
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
    # print(data)
    response = regenerate_sheetmusic(data['chords'], data['scales'], data['title'], data['style'], data['example'], data['regenprompt'])
    try:
        newjam = json.loads(response)
        print(newjam['output'])
        return jsonify({"examplesong": newjam['output']}), 200
    except Exception as e:
        print(f"Failed to load json from response\n {e}")
        print(response)
        return jsonify({"error": e}), 500
    
@app.route('/genharmony', methods=['POST'])
def generate_harmony():
    '''
    Generate a new harmony in ABC notation using few shot prompt engineering with gpt 4
    '''
    data = request.get_json()
    # print(data)
    response = generate_harmony_from_jam(data['chords'], data['scales'], data['title'], data['style'], data['example'])
    try:
        harmony = json.loads(response)
        print(harmony['output'])
        return jsonify({"harmony": harmony['output']}), 200
    except Exception as e:
        print(f"Failed to load json from response\n {e}")
        print(response)
        return jsonify({"error": e}), 500

@app.route('/getchord', methods=['GET'])
def get_chord():
    '''
    Return ABC notation for the specified chord
    '''
    chord = request.args.get('chord')
    abcchord = get_chord_abc(chord)
    print(abcchord)
    try:
        abcchord_dict = json.loads(abcchord)
    except Exception as e:
        print(f"Failed to load json from response\n {e}")
        print(abcchord)
        return jsonify({"error": e}), 500
    finally:
        # Now you can check and access 'abcchord' as expected
        if abcchord_dict and 'abcchord' in abcchord_dict:
            return jsonify({"chord": abcchord_dict['abcchord']}), 200
        else:
            return jsonify({"error": "Chord not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)