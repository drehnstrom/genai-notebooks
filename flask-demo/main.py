from flask import Flask, render_template, request
import markdown
import os
import yaml
import vertexai
from vertexai.language_models import TextGenerationModel
from vertexai.generative_models import (GenerativeModel, GenerationConfig, 
                                        Image, Part, FinishReason)

app = Flask(__name__)

def get_config_value(config, section, key, default=None):
    """
    Retrieve a configuration value from a section with an optional default value.
    """
    try:
        return config[section][key]
    except:
        return default
        
with open('config.yaml') as f:
    config = yaml.safe_load(f)

TITLE = get_config_value(config, 'app', 'title', 'Ask Google')
SUBTITLE = get_config_value(config, 'app', 'subtitle', 'Your friendly Bot')
CONTEXT = get_config_value(config, 'genai', 'context', 'You are a bot who can answer all sorts of questions')
BOTNAME = get_config_value(config, 'genai', 'botname', 'Google')
TEMPERATURE = get_config_value(config, 'genai', 'temperature', 0.8)


@app.route("/", methods = ['POST', 'GET'])
def main():
    if request.method == 'POST':
        input = request.form['input']
        model = request.form['submit']

        if (model == "Gemini"):
            response = get_response_gemini(input) 
        else:
            response = get_response_palm(input)
    else: 
        input = ""
        response = get_response_gemini("Who are you and what can you do?")
    
    response = markdown.markdown(response)
    model = {"title": TITLE, "subtitle": SUBTITLE, "botname": BOTNAME, "message": response, "input": input}
    return render_template('index.html', model=model)


def get_response_gemini(input):
    vertexai.init(location="us-central1")
    
    generationConfig = GenerationConfig(
      temperature=TEMPERATURE,
    )

    model = GenerativeModel("gemini-1.5-flash-001")

    prompt = """{0}.

    input: {1}
    output:
    """.format(CONTEXT, input)
    
    response = model.generate_content(
      [prompt],
      generation_config=generationConfig,
      stream=False,
    )

    return response.text
    


def get_response_palm(input):

    # In the PaLM API, Temperature is between 0.0 and 1.0
    global TEMPERATURE
    if TEMPERATURE > 1.0: 
      TEMPERATURE = 1.0

    vertexai.init(location="us-central1")
    parameters = {
        "temperature": TEMPERATURE,
    }

    model = TextGenerationModel.from_pretrained("text-bison")
    request = """{0}.
    
    input: {1}
    output:
    """
    response = model.predict(
        request.format(CONTEXT, input),
        **parameters
    )
    return response.text
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    
