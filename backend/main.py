from flask import Flask, request
from dotenv import load_dotenv
import os
from openai import OpenAI
import ast
#------------ TASK -------------

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

load_dotenv()
api_key = os.getenv('API_KEY')
client = OpenAI(api_key=api_key)

# Ensure save_words.txt exists
if not os.path.exists('save_words.txt'):
    open('save_words.txt', 'w').close()

app = Flask(__name__)

#--------------INITIAL TEST ROUTES--------------

#ALL ROUTES
# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# @app.route("/testing-input")
# def test_input():
#     name = request.args.get('name', 'No name provided')
#     print(name)
#     return f'<p>{name}<\p>'

#-------------------- FUNCTIONS ---------------

#PARSE RESPONSE (not needed?)
def parse_groupings(response):
    response = response.replace(',', '')
    response = response.replace('[', '')
    response = response.replace(']','')
    words = [i.strip() for i in response.split(' ')]
    
    # Open the file in write mode ('w')
    with open('save_words.txt', 'w') as file:
        for i in range(0, len(words), 4):
            file.write(str(words[i:i+4]))

    return [words[i:i+4] for i in range(0, len(words), 4)]

#CONFIDENCE SCORE
def get_confidence_score(previous_guess, remaining_words):
    prompt = f"After guessing '{previous_guess}' and getting it wrong, how confident are you that your next guess will be correct? The remaining words are {', '.join(remaining_words)}. Please provide a confidence score between 0 and 1."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        confidence_score = float(response.choices[0].message.content.strip())
    except ValueError:
        confidence_score = 0.5
    return confidence_score

#------------------------ ROUTES ---------------

#CALL API, MAKE GROUPINGS 
@app.route("/get-groupings", methods=["GET"])
def get_groupings():

    #Check if already found the answer
    if os.path.getsize('save_words.txt') != 0:
       with open('save_words.txt', 'r') as file:
        first_line = file.readline().strip()
        list_of_lists = ast.literal_eval(first_line)
    
        # Pop the first inner list
        if list_of_lists:
            popped_value = list_of_lists.pop(0)
        else:
            raise ValueError("The list of lists is empty; nothing to pop.")

        # Rewrite the updated list of lists back to the file
        with open('save_words.txt', 'w') as file:
            file.write(str(list_of_lists))
    
        # Return the popped value
        return popped_value

    #get input
    words_input = request.args.get('words', '')
    if not words_input:
        return "<p> No Input</p>"

    #convert into list
    #make sure words are split by , and maybe " ", 16 words only
    words_list = [word.strip() for word in words_input.split(",")]
    if len(words_list) != 16:
        return "<p>Must be exactly 16 words</p>"
    
    # ADD THE WORDS TO THE PROMPT
    prompt = """
    Background: The Connections game from The New York Times (NYT) has become a popular brain teaser, challenging players to associate words based on categories. The objective is to develop a bot capable of effectively categorizing a set of words into four distinct groups based on their connections. You will be given a board of 16 words arranged randomly, and you will have to select the best 4 words possible that match a group for four distinct groups in order to ensure your success. 

    Rules of the Game: 
    Connections AI is a single-player game with 16 words on the board. Each word will only belong to one of the four groups of four. Each group will have four words. Players will start with 4 chances/lives. To play, players will select four words that match a certain category. When a player guesses 3/4 words correctly, the player will receive a one-word-away warning. If they correctly select four words that match one of the four categories, the player will continue to guess the next category. If they select the wrong four words, the player will lose a life. The player wins when all 16 words are correctly matched with their category. Accuracy of guessing groups matters. 

    Categories can be based on any logical associations, such as synonyms, types, functions, or any other common link. The words in the list are:
    Words: {', '.join(words_list)} Your task is to group these 16 words into 4 groups of 4 words each. Ensure that each word is used only once and belongs to a specific group. The categories should be based on logical connections. These could involve occupations, things associated with motion, objects with specific shapes, or anything that could reasonably connect the words together.
    Please categorize the words by selecting four words that belong together under one category and repeat this until all words are categorized. Each category should contain only four words, and no word should appear in more than one category. Make sure the connections between the words in each group are clear, and the categories are logically distinct. You should aim for clarity, logical consistency, and minimal overlap between categories.
    Your response should be in the following format:
    [['word1', 'word2', 'word3', 'word4'],
    ['word5', 'word6', 'word7', 'word8'],
    ['word9', 'word10', 'word11', 'word12'],
    ['word13', 'word14', 'word15', 'word16']]
    Please only provide the output in the exact 4x4 format. Do not include any explanations, reasoning, or additional commentary. Only provide the list of grouped words that satisfy the above requirements. Again, the final output should be presented as exactly four groups of four words, and no word should be repeated or omitted.
    """


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

#DO GAME (WITH LIVES, CONFIDENCE)
@app.route("/game", methods=["GET"])
def game():
    words_input = request.args.get('words', '')
    words_list = [word.strip() for word in words_input.split(",") if word.strip()]

    if len(words_list) != 16:
        return "<p>Must be exactly 16 words</p>"

    lives = 4
    strikes = 0
    correct_guesses = []

    while lives > 0 and len(correct_guesses) < 16:
        guesses = {}
        for word in words_list:
            if word not in correct_guesses:
                prompt = f"After guessing '{word}', how confident are you that this word fits into the correct category? (Please give a score between 0 and 1)."
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                try:
                    confidence = float(response.choices[0].message.content.strip())
                    guesses[word] = confidence
                except ValueError:
                    guesses[word] = 0.5  # Default confidence if there's an issue with the response

        best_guess = max(guesses, key=guesses.get)
        highest_confidence = guesses[best_guess]

        if highest_confidence >= 0.92:
            correct_guesses.append(best_guess)
        else:
            strikes += 1
            if strikes >= 4:
                lives -= 1
                strikes = 0

    if len(correct_guesses) == 16:
        return f"<p>You won! All words guessed correctly: {', '.join(correct_guesses)}</p>"
    else:
        return f"<p>Game Over! You have {lives} lives left.</p>"


if __name__ == "__main__":
    app.run(debug=False)