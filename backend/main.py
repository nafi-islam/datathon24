from flask import Flask, request
from dotenv import load_dotenv
import os


app = Flask(__name__)

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

#make route, use opanAI API for python, ask Nafi for API key, create .env file, 
#make and add to git ignore, copy paste API key, make request, 
# return ans yas, 
# function with open AI API, make call, method passes to the prompt w/ prompt engr, API clal function
# parse the response, get the grouping, make into array 

#make secrets.txt, add .gitignore, then import api key from secrests make it a variable in code.
#with read, with open " " file, parse line, get API key, save as variable
load_dotenv()
api_key = os.getenv('api_key')
from openai import OpenAI
client = OpenAI(os.getemv(api_key))

response = client.chat.completions.create(
    messages=[{
        "role": "user",
        "content": "Say this is a test",
    }],
    model="gpt-4o-mini",
)

print(response._request_id)