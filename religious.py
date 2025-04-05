import base64
import os
from google import genai
from google.genai import types


def generate(history):
    client = genai.Client(
        api_key="AIzaSyA3CIQ94sdwOf0NwIaXKcAeatOI6acYPhQ",
    )

    model = "gemini-2.0-flash"
    contents = history
    tools = [
        types.Tool(google_search=types.GoogleSearch())
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0,
        tools=tools,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""you are a religious ai and are designed to talk to older people and answer to their religious questions in an understandable way. do this only using ascii characters"""),
        ],
    )
    s=''
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        s+=chunk.text
    return s

'''user=input('User: ')
history=[types.Content(role="user",parts=[types.Part.from_text(text=user),],)]
while user!='Quit':
    out=generate(history)
    history+=[types.Content(role="model",parts=[types.Part.from_text(text=out)])]
    print()
    print('AthenAI:',out)
    user=input('User: ')
    if user!='Quit':
        history+=[types.Content(role="user",parts=[types.Part.from_text(text=user)])]
'''