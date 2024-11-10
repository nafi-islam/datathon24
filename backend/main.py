from flask import Flask, request
from dotenv import load_dotenv
import os
#from openai import OpenAI
import openai

#TASK:
#make a route, use Open AI API, create API key and hide in .env file, use gitignore
#Function 1: Use API, make a call, take in a 1D array, method passes to the prompt (use prompt engr), API call function 
#Function 2: parse the response, get the grouping, make and return into an array
#make and add to git ignore, copy paste API key, make request

#GIT COMMANDS (uwu)
#git add . 
#git status
#git commit -m "name"
#git push
#git status
#git log
#git pull
#git checkout -b "name" (create branch)
#git push origin Niki-dev

#load env variables
load_dotenv()

#get key + check
api_key = os.getenv('API_KEY')
openai.api_key = api_key; #set the API key

#---------INITIAL TEST ROUTES---------

#initialize clinet + flask
#client = OpenAI(api_key)
app = Flask(__name__)

#ALL ROUTES
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/yo")
def yo_world():
    return "<p>Yo!<p>"

@app.route("/testing-input")
def test_input():
    name = request.args.get('name', 'No name provided')
    print(name)
    return f'<p>{name}<p>'

#----------- FUNCTIONS --------------

#FUNCTION 1
#Function 1: Use API, make a call, take in a 1D array, method passes to the prompt (use prompt engr), API call function 
@app.route("/get-groupings", methods=["GET"])
def get_groupings():
    #get input
    words_input = request.args.get('words', '')
    if not words_input:
        return "<p> No Input<p>"

    #convert into list
    #make sure words are split by , and maybe " ", 16 words only
    words_list = [word.strip() for word in words_input.split(",")]
    if len(words_list) != 16:
        return "<p>Must be exactly 16 words<p>"

    #PROMPT ENGR for chatGPT to use
    #WILL NEED TO CHANGE PROMPT (play around with gpt)
    prompt = f"Categorize these words into 4 groups of 4 words each similar to the New York Times Connections Game: {', '.join(words_list)}"

    # Make API call
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Ensure you are using the correct model
        messages=[{
            "role": "user",
            "content": prompt,
        }],
    )

    #print response
    print(f"Request ID: {response['id']}")


#FUNCTION 2
#Function 2: parse the response, get the grouping, make and return into an array



