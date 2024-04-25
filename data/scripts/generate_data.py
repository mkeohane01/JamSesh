from openai import OpenAI
from dotenv import load_dotenv
import openai
import json
import os
import argparse
from generation_list import jam_inputs, jam_inputs_2

def query_gpt(prompt, model="gpt-4-1106-preview", max_tokens=500, temperature=1, top_p=1, frequency_penalty=0, presence_penalty=0):
    """
    Generate Various Chord Progressions, Improvisation Scales, and example using in ABC notation
    using the OpenAI API.

    Args:
        prompt (str): Prompt for the OpenAI API

    Returns:
        response (str): Response from the OpenAI API
    """
    # OpenAI Client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # OpenAI Completion API
    response = client.chat.completions.create(model=model,
                                            messages=[
                                                {"role": "system", "content": "Act as an expert musician specifically good at improvisation with accompanying chord progressions. You have to generate Jam Session recommendations in properly formatted JSON. This inlcudes recommended chords, recommended scales, and example song in ABC notation"},
                                                {"role": "user", "content": prompt}],
                                            response_format={ "type": "json_object" },
                                            temperature=temperature,
                                            max_tokens=max_tokens,
                                            top_p=top_p,
                                            frequency_penalty=frequency_penalty,
                                            presence_penalty=presence_penalty
                                        )

    return response.choices[0].message.content.strip()

def create_prompt_for_jamsesh(input):
    """
    Create a prompt for the OpenAI API that allows for creative musical recommendations using ABC notation.
    
    Returns:
        prompt (str): Prompt for the OpenAI API
    """
    return f"""Sample JamSesh input / output pairs in JSON format for few shot learning. Strictly follow the format for the output! 
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
                "scales": "Dm Pentatonic (D F G A C)",
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

    Follow the following format for the output for query {input} exactly just like the examples above: 
    Strictly output in this JSON format for this {input}

    "input": "{input}",
    "output": {{
        "chords": "## Suggested chord progression",
        "scales": "## Suggested scale for improvising",
        "title": "## Title of Jam",
        "style": "## Style to play like",
        "example": "## ABC notation for an example section using these chords and notes"
    }}
    """

def generate_data(inputs_list=jam_inputs, outputfolder="data/jamseshGPT4"):
    """
    Create a dataset of JamSesh IO using the OpenAI Chat Completions API.
    Args:
        inputs_list (list): List of input for the JamSesh prompt
        outputfolder (str): Folder to save the generated data
    Returns:
        None
    """

    # Iterate through the files in the folder
    for i, input in enumerate(inputs_list):
        # Create the jam prompt
        prompt = create_prompt_for_jamsesh(input)

        # Generate the JamSesh output JSON
        gen_jam = query_gpt(prompt, model="gpt-4-turbo")

        try:
            # Convert the string response to a Python Dict object
            output_list = json.loads(gen_jam)

            # Save the generated data as a JSON file
            with open(f"{outputfolder}/jamsesh_{50+i}.txt", 'w') as txt_file:
                txt_file.write(json.dumps(output_list))
        except:
            # Save the generated data as a JSON file
            print("unable to load json")
            with open(f"{outputfolder}/jamsesh_{50+i}.txt", 'w') as txt_file:
                txt_file.write(gen_jam)

        print(f"Just finished rep {i}")
        
if __name__ == '__main__':
    # Load the .env file with the API key
    load_dotenv()

    # Generate the JamSesh data
    generate_data(jam_inputs_2, outputfolder="data/jam_gpt4gens")