# Gemini API Flask App Demo

This demo is a Python Flask web app that uses the Google Gemini API for generative AI.

## To Run
1. Clone the repo
2. Change to the app folder (it should be `~/genai-notebooks/flask-demo`)
3. Run the following to create a Virtual Environment:

```
pip install virtualenv
virtualenv ~/genai-virtual-env
source ~/genai-virtual-env/bin/activate
```

3. Use Pip to install the prequisites

```
pip install -r requirements.txt
```

4. To test the pogram run:

```
python main.py
```

## You can customize the program using the config.yaml file.

Here is an example. Changing the context will change the bahavior of the model. You can make the model pretend to be anything you want (a bartender, mechanic, whatever). The example below makes the model emulate a Barista. 

Change the YAML file and restart the program

```
app:
 title: "CoffeeBot"
 subtitle: "Your friendly online BaristAI"

palm:
  botname: "CoffeeBot"
  context: "Your name is CoffeeBot. You are a barista and expert on all things related to coffee and tea."
  temperature: 0.8
```

The variable temperature controls how creative (random) the model will be when answering. Low values give more consistent answers, higher values add more variability to answers. 

temperature is in the range 0.0 to 2.0. (For older models it was between 0.0 and 1.0)