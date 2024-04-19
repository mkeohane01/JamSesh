from openai import OpenAI
import os
from dotenv import load_dotenv
import json


def build_fewshot_prompt(prompt):
    """
    Create a prompt for the OpenAI API that allows for creative musical recommendations using ABC notation though few shot.
    Input: 
        user prompt
    Returns:
        prompt (str): Prompt for the OpenAI API
    """
    return f"""Sample JamSesh input / output pairs in JSON format for few shot learning. Strictly follow the format for the input and output! 
    The "example" is in ABC notation (sharp noted by ^ and flat by _ before the note) Think about the music theory behind the chords and scales.:
    [
        {{
            "input": "Generate a Jam in a classic Blues fashion", 
            "output": {{
                "chords": "E7 | A7 | E7 | E7 | A7 | A7 | E7 | E7 | B7 | A7 | E7 | B7",
                "scales": "E Mixolydian (E F# G# A B C# D#)",
                "title": "Classic 12-Bar Blues in E",
                "style": "Focus on a strong, steady beat with a slight shuffle to emphasize the blues feel. Ideal for expressive bends and vibrato.",
                "example": `
                M:4/4
                L:1/8
                Q:120
                K:E
                |: "E7" EG  A2 z2 A2  | "A7" A,4 C2 D2 | "E7"E2 A2 BCDE | "E7"E4 z4 |
                    "A7"A,3 z C4 | "A7" A,B,A,B, C2 D2| "E7"E4 B,2 E2 | "E7"E6 z2 |
                    "B7"B4 D'4 | "A7"A,4 C4 | "E7"E4 D2 E2 | "B7"B,4 z ABC'D' :|
                `
            }}
        }},
        {{
            "input": "Funky groovy jam in C major",
            "output": {{
                "chords": "C7 | F7 | G7 | C7 | C7 | F7 | G7 | C7",
                "scales": "C Mixolydian (C D E F G A B)",
                "title": "Funky Groove Jam in C",
                "style": "A funky, upbeat feel with a strong backbeat to emphasize movement. Ideal for tight, rhythmic playing and lively bass lines.",
                "example": `
                M:4/4
                L:1/8
                Q:100
                K:C
                |: "C7"CDEFGAGF | "F7"F2A2c2d2 | "G7"G2B2d2G2 | "C7"C4E2G2 |
                "C7"C2D2E2F2 | "F7"A4c2A2 | "G7"BAGFEDC2 | "C7"C8 :|
                |: "C7"C2C2E2G2 | "F7"F2A2A2c2 | "G7"G2B2d2e2 | "C7"C2E2G2C2 |
                "C7"c2c2e2g2 | "F7"f2a2c'2a2 | "G7"g2b2d'2b2 | "C7"c8 :|
                `
            }}
        }},
        {{
            "input": "Soul jazzy blues feel",
            "output": {{
                "chords": "Dm7 | Gm7 | Dm7 | Dm7 | Gm7 | Gm7 | Dm7 | Dm7 | Am7 | Gm7 | Dm7 | Am7",
                "scales": "Dm Dorian (D E F G A Bb C)",
                "title": "Soultown Blues in D",
                "style": "Express a deep, soulful feel with a touch of blues. Aim for a smooth, emotional rendition, making use of the Dorian mode for a slightly melancholic but rich sound.",
                "example": `
                M:4/4
                L:1/8
                Q:80
                K:Dmin
                |: "Dm7"D4 F2 A2 | "Gm7"G2 B2 d4 | "Dm7"D2 E2 F2 D2 | "Dm7"D2 F2 A2 G2 |
                "Gm7"G3 A B2 d2 | "Gm7"B,2 D2 G2 F2 | "Dm7"D3 E F2 A2 | "Dm7"D2 F2 A2 c2 |
                "Am7"A2 c2 E2 c2 | "Gm7"G2 B2 d3 e | "Dm7"D2 F2 A2 d2 | "Am7"A2 c2 A2 E2 :|
                `
            }}
        }},
        {{
            "input": "Driving classic rock jam",
            "output": {{
                "chords": "A | D | A | A | D | D | A | A | E | D | A | E",
                "scales": "A Major (A B C# D E F# G#)",
                "title": "Classic Rock Jam in A",
                "style": "Focus on driving rhythms and powerful chord strikes. Ideal for energetic and expressive piano melodies.",
                "example": `
                M:4/4
                L:1/8
                Q:145
                K:A
                |: "A"A2 E2 F2 E2 | "D"D4 F2 A2 | "A"A,2 A,2 C2 E2 | "A"A4 z4 |
                "D"D F A D F A | "D"D2 F2 A3 z | "A"A, E A, E A, C' E | "A"A,4 E4 |
                "E"E2 B, E2 G2 B, | "D"D4 F2 A2 | "A"A,2 C2 E2 A2 | "E"B,2 E2 G2 B,2 :|
                `
            }}
        }},
        {{
            "input": "Exotic funk rock",
            "output": {{
                "chords": "Gm7 | Cm7 | D7 | Gm7 | Gm7 | Cm7 | F7 | Gm7",
                "scales": "Gm Dorian (G A Bb C D Eb F)",
                "title": "Exotic Funk-Rock Groove in Gm",
                "style": "Combine the driving rhythms of rock with the syncopation of funk, utilizing modal interchange and extended chords for an exotic texture.",
                "example": `
                M:4/4
                L:1/8
                Q:120
                K:Gmin
                |: "Gm7" G2 B3 ABAG | "Cm7" CBAG FGAB 
                | "D7" DEFG FEDC | "Gm7" G2 B2 dcBA | 
                "Gm7" gfga bagf | "Cm7" cBcd edcB 
                | "F7" FGAB cBAG | "Gm7" G4 B2 d2 :|
                `
            }}
        }},
    ]

    Follow the following format for the output for query {prompt} exactly just like the examples above: 
    Strictly output in this JSON format for this {prompt}

    "input": "{prompt}",
    "output": {{
        "chords": "## Suggested chord progression",
        "scales": "## Suggested scale for improvising",
        "title": "## Title of Jam",
        "style": "## Style to play like",
        "example": "## ABC notation for an example section using these chords and notes"
    }}
    """

def query_gpt(prompt, model="gpt-4-0125-preview", json=True, temperature=1, max_tokens=400):
    """
    Call the OpenAI API to generate a response based on the prompt.

    Args:
        prompt (str): Prompt for the OpenAI API

    Returns:
        response (str): Response from the OpenAI API
    """
    # OpenAI Client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response_type = "json_object" if json else "text"
    # OpenAI Completion API
    response = client.chat.completions.create(model=model,
                                            messages=[{"role": "user", "content": prompt}],
                                            response_format={ "type": f"{response_type}" },
                                            temperature=temperature,
                                            max_tokens=max_tokens,
                                            frequency_penalty=0,
                                            presence_penalty=0
                                        )

    return response.choices[0].message.content.strip()


def generate_jam_from_gpt(prompt, model="gpt-4-0125-preview", temperature=1, max_tokens=500):
    """
    Generate Various Chord Progressions, Improvisation Scales, and example song in ABC notation
    using the OpenAI API based on few shot prompt.

    Args:
        prompt (str): Prompt for the OpenAI API

    Returns:
        response (str): Response from the OpenAI API
    """
    few_shot_prompt = build_fewshot_prompt(prompt)
    
    response = query_gpt(few_shot_prompt, model, json=True, temperature=temperature, max_tokens=max_tokens)
    return response

def regenerate_sheetmusic(chords, scales, title, style, example_song, prompt):
    '''
    Using the chords and recommended scale, regenerate the sheet music for the Jam Session

    Args:
        chords (str): Suggested chord progression
        scales (str): Suggested scale for improvising
        title (str): Title of Jam
        style (str): Style to play like
        example_song (str): ABC notation for an example section using these chords and notes
    Returns:
        sheetmusic (str): Sheet music for the Jam Session in ABC notation
    '''

    sheetmusic_prompt = f"""
        Generate sheet music for a Jam Session using ABC Notation in the style of {title}:{style} 
        using the following chord pogression: {chords} and the recommended improvisation scale: {scales}.
        The response should be a JSON and exactly like format notation like these 2 examples. 
        {{ output: 
            M:4/4 
            L:1/8 
            Q:120
            K:A
            |: "A7"A4 e4 | "D7"d4 f4 | "A7"A4 c4 | "A7"A4 e4 |
            "D7"D4 f4 | "D7"D4 f4 | "A7"A4 c4 | "A7"A4 e4 |
            "E7"E4 g4 | "D7"d4 f4 | "A7"A4 c4 | "E7"E4 g4 :|
        }},
        {{ output: 
            M:4/4
            L:1/8
            Q:100
            K:Gmin
            |: "Gm7" G2 B3 ABAG | "Cm7" CBAG FGAB 
            | "D7" DEFG FEDC | "Gm7" G2 B2 dcBA | 
            "Gm7" gfga bagf | "Cm7" cBcd edcB 
            | "F7" FGAB cBAG | "Gm7" G4 B2 d2 :|
        }}
        The current song generated is CURRENT SONG: { example_song } .
        Make a new melody to go along with those chords: {chords} and using the scale {scales}. Be creative, think about the music theory, choose exciting rythmns and musical phrases,
        and make sure to update the current song according to this user prompt {prompt}. Respond in this exact format, JSON ABC notation.
        """
    response = query_gpt(sheetmusic_prompt, model="gpt-4-0125-preview", json=True, temperature=1, max_tokens=600)
    return response

def generate_harmony_from_jam(chords, scales, title, style, example_song, prompt=''):
    '''
    Add harmony to the melody using the chords and recommended scale

    Args:
        chords (str): Suggested chord progression
        scales (str): Suggested scale for improvising
        title (str): Title of Jam
        style (str): Style to play like
        example_song (str): ABC notation for an example section using these chords and notes
    Returns:
        sheetmusic (str): Sheet music for the Jam Session in ABC notation
    '''

    sheetmusic_prompt = f"""
        Generate sheet music for a Jam Session using ABC Notation in the style of {title}:{style} 
        using the following chord pogression: {chords} and the recoomended improvisation scale: {scales}.
        The response should be a JSON and in the no-X ABC format notation like these 2 examples. 
        {{ output: 
            M:4/4 
            L:1/8 
            Q:120
            K:A
            clef=bass
            |: "A"[ce][ce][ce][ce] [ce][ce][ce][ce] | "D"[Ad][Ad][Ad][Ad] [Ad][Ad][Ad][Ad] | "E"[Be][Be][Be][Be] [Be][Be][Be][Be] | "A"[ce][ce][ce][ce] [ce][ce][ce][ce] |
            "A"[ce][ce][ce][ce] [ce][ce][ce][ce] | "D"[Ad][Ad][Ad][Ad] [Ad][Ad][Ad][Ad] | "E"[Be][Be][Be][Be] [Be][Be][Be][Be] | "A"[ce][ce][ce][ce] [ce][ce][ce][ce] :|
        }},
        {{ output:
            M:4/4
            L:1/8
            Q:110
            K:Dmin
            V:1 clef=treble
            |: "Dm9"D2 F2 A2 C2 | "G13"G,2 B,2 D2 F2 | "Cmaj7"C2 E2 G2 B2 | "Am7"A2 CE A2 c2 :|
            |: "Dm9"d4 c2 A2 | "G13"G,3 A B2 D2 | "Cmaj7"C2 E2 G4 | "Am7"A2 c2 e2 a2 :| .
            V:2 clef=bass
            |: "Dm9"D,4 F,4 | "G13"G,4 B,2 F2 | "Cmaj7"C,4 E,4 | "Am7"A,4 C4 :|
            |: "Dm9"D,2 F,A, D2 F2 | "G13"G,,2 G,2 B,2 D2 | "Cmaj7"C,2 E,G, C2 E2 | "Am7"A,2 C2 E2 A2 :| 
        }}
        The current song generated is { example_song } .
        Make a corresponding harmony using these chords: {chords} and to support this scale {scales}. 
        Be creative, and make sure to have the hamony support the current song and be outputted in the correct notation.
        """
    response = query_gpt(sheetmusic_prompt, model="gpt-4-0125-preview", json=True, temperature=1, max_tokens=600)
    return response

def get_chord_abc(chord):
    '''
    Return ABC notation for the specified chord

    Args:
        chord (str): Chord to return in ABC notation
    Returns:
        ABC notation for the specified chord
    '''
    prompt = f"""Return strictly in ABC notation (sharp noted by ^ and flat by _ before the note along with chord by []) for the entire chord {chord}. Think about what notes are in that particular chord! 
    Examples - 
    input: 'C7' returns: {{abcchord: '\"C7\"  [C E G _B] '}} 
    input:'G' returns: {{ abcchord: '\"G\"  [G B D]' }} 
    input:'Dm' returns: {{ abcchord: '\"Dm\"  [D F _B]' }}
    input:'D5' returns: {{ abcchord: '\"D5\"  [D ^F B]' }} 
    input:'F#' returns: {{ abcchord: '\"F#\"  [^F ^A ^C]' }}
    input:'Bb' returns: {{ abcchord: '\"Bb\"  [_B D F]' }}
    input: 'D7' returns: {{ abcchord: '\"D7\"  [D ^F A C]' }}
    input: 'Dm7 A7' returns: {{ abcchord: '\"Dm7 A7\"  [D F A C] [A ^C E G]' }}
    input: 'Gm7' returns: {{ abcchord: '\"Gm7\"  [G _B D F]' }}
    Now in same style as the examples, return the strict ABC notation for the chord {chord} as a JSON."""
    response = query_gpt(prompt, model="gpt-4-0125-preview", json=True, temperature=1, max_tokens=200)
    return response

if __name__ == "__main__":
    load_dotenv()
    prompt = "Groovy blues, jazz style. 16 bar progression"
    response = generate_jam_from_gpt(prompt)
    print(response)
    response_json = json.loads(response)
    print(response_json["output"])
