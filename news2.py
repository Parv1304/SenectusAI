from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=("[API KEY HERE]"),
    )

    model = "gemini-2.0-flash"
    contents = [types.Content(role = "user", parts = [types.Part.from_text(text = 'follow your predefined system instructions and generate news'),],)]
    tools=[types.Tool(google_search=types.GoogleSearch())]
    generate_content_config = types.GenerateContentConfig(
        temperature=0,
        tools=tools,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""You are an expert news reporter who has the following objectives:
                                 DOs:-
                                 1. Generate 5 main headlines with sufficient elaboration.
                                 2. Include only 5 subpoints in each main headline.
                                 3. Be natural, fluent in your speech.]
                                 4. The tranistions to the next headline should be natural.
                                 
                                 DONT's:-
                                 1. Use bold or italics.
                                 2. Generate any text other than the headlines.
                                 3. Use characters outside the ascii range.  """),
        ],
    )
    s =''
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        s += chunk.text
    return s
