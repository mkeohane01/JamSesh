from openai import OpenAI
from dotenv import load_dotenv
import openai
import json
import os
import argparse

def generate_jam_sesh_recommendation(prompt, model="gpt-4-1106-preview", max_tokens=3500, temperature=1, top_p=1, frequency_penalty=0, presence_penalty=0):
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

def create_prompt():
    """
    Create a prompt for the OpenAI API that allows for creative musical recommendations using ABC notation.
    
    Returns:
        prompt (str): Prompt for the OpenAI API
    """
    return f"""Sample JamSesh input / output pairs:
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

    Now create JamSesh recommendations in a similar way for the various blues, jazz, funk, and rock genres. 

    Please use creativity by using unique rythmns, keys, genres, and styles! Generate jams of different styles and genres! 

    Generate 5 unique input, output pairs each with unique sounds yet stay consistent to the style and genre of the music with their chord progressions and corresponding scale.

    Follow the following format for the final output exactly just like the examples above:

    [
        {{
            "input": "## Style and genre to generate a jam session / song about",
            "output": {{
                "chords": "## Suggested chord progression",
                "scales": "## Suggested scale for improvising",
                "title": "## Title of Jam",
                "style": "## Style to play like",
                "example": `
                    ## ABC notation for an example section using these chords and notes
                `,
            }}
        }}
        {{
            "input": "## Style and genre to generate a jam session / song about",
            "output": {{
                "chords": "## Suggested chord progression",
                "scales": "## Suggested scale for improvising",
                "title": "## Title of Jam",
                "style": "## Style to play like",
                "example": `
                    ## ABC notation for an example section using these chords and notes
                `,
            }}
        }},
    ]
    """

def create_dataset(outputfile="./data/stf_data.json"):
    """
    Create a dataset of JamSesh IO using the OpenAI Chat Completions API.
    Args:
        outputfile
    Returns:
        None
    """

    # Iterate through the files in the folder
    for i in range(100):
        # Create theprompt
        prompt = create_prompt()

        # Generate Adverse Event Reports for the Drug
        reports = generate_jam_sesh_recommendation(prompt, model="gpt-4-1106-preview")

        try:
            # Convert the string response to a Python Dict object
            output_list = json.loads(reports)

            # Save the generated data as a JSON file
            with open(f"data/gpt4gen/jamseshio{i}.txt", 'w') as txt_file:
                txt_file.write(json.dumps(output_list))
        except:
            # Save the generated data as a JSON file
            print("unable to load json")
            with open(f"data/gpt4gen/jamseshio{i}.txt", 'w') as txt_file:
                txt_file.write(reports)

        print(f"Just finished rep {i}")
        
if __name__ == '__main__':
    # Load the .env file with the API key
    load_dotenv()

    # Parse the arguments
    # parser = argparse.ArgumentParser(description="Data Preparation Script")
    # parser.add_argument('--folder-path', type=str, default='data/raw_drug_info/', help="Path to the folder containing the raw Drug Information files scraped form web")
    # args = parser.parse_args()

    # Create the folder if it doesn't exist
    # if not os.path.exists(args.folder_path):
    #     os.makedirs(args.folder_path)

    create_dataset()