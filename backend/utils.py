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
    return f"""Sample JamSesh input / output pairs in JSON format for few shot learning:
    [
        {{
            "input": "Generate a Jam in a classic Blues fashion", 
            "output": {{
                "chords": "E7 | A7 | E7 | E7 | A7 | A7 | E7 | E7 | B7 | A7 | E7 | B7",
                "scales": "E Mixolydian (E F# G# A B C# D)",
                "title": "Classic 12-Bar Blues in E",
                "style": "Focus on a strong, steady beat with a slight shuffle to emphasize the blues feel. Ideal for expressive bends and vibrato.",
                "example": `
                M:4/4
                L:1/8
                K:E
                |: "E7"E4 B2 z2 | "A7"A,6 C2 | "E7"E4 ^D2 E2 | "E7"E4 z4 |
                "A7"A,4 C4 | "A7"A,6 C2 | "E7"E4 B,2 E2 | "E7"E6 z2 |
                "B7"B,4 ^D4 | "A7"A,4 C4 | "E7"E4 ^D2 E2 | "B7"B,4 z4 :|
                `
            }}
        }},
        {{
            "input": "Jazzy, Bluesy feel",
            "output": {{
                "chords": "G7 | C7 | G7 | G7 | C7 | C7 | G7 | E7 | Am7 | D7 | G7 E7 | Am7 D7",
                "scales": "G Mixolydian (G A B C D E F)",
                "title": "Jazz-Blues in G",
                "style": "Adopt a smooth, laid-back groove with plenty of room for chromatic runs and jazz phrasing. Highlight the swing feel in your rhythm section.",
                "example": `
                M:4/4
                L:1/8
                K:G
                |: "G7"G4 B2 d2 | "C7"c4 E2 G2 | "G7"G4 D2 G2 | "G7"G4 z4 |
                "C7"c4 E4 | "C7"c4 E2 G2 | "G7"G4 B2 d2 | "E7"E4 ^G2 A2 |
                "Am7"A4 c2 e2 | "D7"d4 F2 A2 | "G7"G4 B2 d2 | "Am7"A2 "D7"d2 "G7"G4 :|
                `
            }}
        }},
        {{
            "input": "Minor blues style jam",
            "output": {{
                "chords": "Am7 | Dm7 | Am7 | Am7 | Dm7 | Dm7 | Am7 | Am7 | F7 | E7 | Am7 | E7",
                "scales": "A Dorian (A B C D E F# G)",
                "title": "Minor Blues in A",
                "style": "Play with a more introspective, soulful mood. Use the minor scale to explore moody, expressive solos and deep grooves.",
                "example": `
                M:4/4
                L:1/8
                K:Am
                |: "Am7"A4 E2 A2 | "Dm7"d4 F2 A2 | "Am7"A4 c2 e2 | "Am7"A6 z2 |
                "Dm7"d4 F2 A2 | "Dm7"d4 F2 A2 | "Am7"A4 E2 A2 | "Am7"A4 z4 |
                "F7"F4 A2 c2 | "E7"E4 G2 B2 | "Am7"A4 c2 e2 | "E7"E4 ^D4 :|
                `
            }}
        }},
        {{
            "input": "Swing Jazz, bluesy syle",
            "output": {{
                "chords": "C6 | F9 | C6/A | G7 | F9 | F#dim7 | C6/A | A7 | Dm7 | G7 | C6 A7 | Dm7 G7",
                "scales": "C Mixolydian (C D E F G A Bb)",
                "title": "Swing Blues in C",
                "style": "Emphasize the swing rhythm, creating a bouncy, energetic feel. Perfect for trading fours and building dynamic solos.",
                "example": `
                M:4/4
                L:1/8
                K:C
                |: "C6"C4 E2 G2 | "F9"F4 A2 c2 | "C6/A"A4 G4 | "G7"G4 B2 d2 |
                "F9"F4 A2 c2 | "F#dim7"F4 A2 c2 | "C6/A"A4 G4 | "A7"A4 c2 e2 |
                "Dm7"D4 F2 A2 | "G7"G4 B2 d2 | "C6"C4 E2 G2 | "Dm7"D2 "G7"G2 "C6"C4 :|
                `
            }}
        }},
        {{
            "input": "Jam session using a Funky jazz syle",
            "output": {{
                "chords": "F7 | Bb7 | F7 | Cm7 F7 | Bb7 | Bdim7 | F7 | D7 | Gm7 | C7 | F7 D7 | Gm7 C7",
                "scales": "F Mixolydian (F G A Bb C D E♭)",
                "title": "Funky Blues in F",
                "style": "Lay down a groove with tight, syncopated rhythms. Focus on the interaction between the rhythm section and the lead, making space for funky riffs and stabs.",
                "example": `
                M:4/4
                L:1/8
                K:F
                |: "F7"F4 A2 c2 | "Bb7"B4 d2 f2 | "F7"F4 A2 c2 | "Cm7"C4 E2 G2 "F7"F4 |
                "Bb7"B4 d2 f2 | "Bdim7"B4 d2 f2 | "F7"F4 A2 c2 | "D7"D4 F2 A2 |
                "Gm7"G4 B2 d2 | "C7"C4 E2 G2 | "F7"F4 A2 c2 | "D7"D2 "Gm7"G2 "C7"C4 :|
                `
            }}
        }},
    ]

    Follow the following format for the output for query {prompt} exactly just like the examples above:

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

def regenerate_sheetmusic(chords, scales, title, style, example_song, prompt=None):
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
        Generate sheet music for a Jam Session using ABC Notation in the style of {title} 
        using the following chord pogression: {chords} and the recoomended improvisation scale: {scales}.
        The response should be a JSON and in the no-X ABC format notation exactly like these examples. 
        {{ output: `{example_song}` }}
        or
        {{ output: 
            `
            M:4/4 
            L:1/8 
            K:A
            %Harmony
            V:1
            |: "A7"A4 e4 | "D7"d4 f4 | "A7"A4 c4 | "A7"A4 e4 |
            "D7"D4 f4 | "D7"D4 f4 | "A7"A4 c4 | "A7"A4 e4 |
            "E7"E4 g4 | "D7"d4 f4 | "A7"A4 c4 | "E7"E4 g4 :|
            %Melody
            V:2
            |: "A7"A2 B2 C2 E2 | "D7"F2 d2 F2 A2 | "A7"A2 c2 E2 A2 | "A7"A4 B2 c2 |
            "D7"D2 F2 A2 d2 | "D7"D2 F2 A2 d2 | "A7"A2 E2 c2 A2 | "A7"A4 B2 c2 |
            "E7"e2 G2 B2 e2 | "D7"F2 A2 d2 F2 | "A7"A2 B2 c2 A2 | "E7"E4 G2 B2 :|
            ` 
        }}
            
        Make a new 8-24 bar melody to go along with those chords: {chords} and and scales {scales}. Be creative, choose exciting rythmns and musical phrases.
        """
    response = query_gpt(sheetmusic_prompt, model="gpt-4-0125-preview", json=True, temperature=1, max_tokens=600)
    return response


if __name__ == "__main__":
    load_dotenv()
    prompt = "Groovy blues, jazz style. 16 bar progression"
    response = generate_jam_from_gpt(prompt)
    print(response)
    response_json = json.loads(response)
    print(response_json["output"])
