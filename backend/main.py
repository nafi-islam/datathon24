from flask import Flask, request
from dotenv import load_dotenv
import os
#from openai import OpenAI
import unittest
from openai import OpenAI, AsyncOpenAI
#import asyncio

#------------ TASK -------------

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

client = OpenAI(api_key=api_key)


#---------INITIAL TEST ROUTES------------

#initialize clinet + flask
#client = OpenAI(api_key)
app = Flask(__name__)

#ALL ROUTES
# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# @app.route("/yo")
# def yo_world():
#     return "<p>Yo!<p>"

@app.route("/testing-input")
def test_input():
    name = request.args.get('name', 'No name provided')
    print(name)
    return f'<p>{name}<p>'

#-------------- FUNCTIONS ---------------

#FUNCTION 2
#Function 2: parse the response, get the grouping, make and return into an array
def parse_groupings(response):
    response = response.replace(',', '')
    response = response.replace('[', '')
    response = response.replace(']','')
    words = [i.strip() for i in response.split(' ')]

    groups = [words[i:i+4] for i in range(0, len(words), 4)]
        

    #for line in lines:
    #    if line.startswith("Group"):
    #        words = line.split(":")[1].strip().split(",")
    #        groups.append([word.strip() for word in words])
    
    return groups

#FUNCTION 1
#Function 1: Use API, make a call, take in a 1D array, method passes to the prompt (use prompt engr), API call function 
@app.route("/get-groupings", methods=["GET"])
def get_groupings():
    #get input
    words_input = request.args.get('words', '')
    if not words_input:
        return "<p> No Input</p>"

    #convert into list
    #make sure words are split by , and maybe " ", 16 words only
    words_list = [word.strip() for word in words_input.split(",")]
    if len(words_list) != 16:
        return "<p>Must be exactly 16 words</p>"

    # chatgpt prompt
    prompt = (
        f"Please group the following words into groups of 4 in a logical way to beat the game Connections: {', '.join(words_list)}. Provide the groups as a list of 4 lists of the grouped words. Do not say anything else. Only give the list. Example: '[[object 1, object 2, object 3, object 4], [object 1, object 2, object 3, object 4], [object 5, object 6, object 7, object 8], [object 9, object 10, object 11, object 12]]'. Do not add quotation marks."
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        print(str(completion.choices[0].message.content))
        response_content = completion.choices[0].message.content
        groups = parse_groupings(response_content)
        return f'<p>Grouped Words: {groups}</p>'

    except Exception as e:
        return f"<p>Error: {e}</p>"

if __name__ == "__main__":
    app.run(debug=True)



#use confdenct score , judge based on if its confident enough, if not confident try again