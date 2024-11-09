from flask import Flask, request
from dotenv import load_dotenv
import os
from openai import OpenAI

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

#load env variables
load_dotenv()

#get key + check
api_key = os.getenv('api_key')
#print(f"API Key Loaded: {api_key}")

#initialize clinet + flask
client = OpenAI(api_key)
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

#OPEN AI API
@app.route("/get-response", methods=["GET"])
def get_response():
    #take user input from 'input'
    user_input = request.args.get('input', '')

    #make API call
    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": "Say this is a test",
        }],
        model="gpt-4o-mini",
    )
    #print request ID (do i need this?)
    print(response._request_id)

    #returns response
    return f"<p>{response['choices'][0]['message']['content']}</p>"