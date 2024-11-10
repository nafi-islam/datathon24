import asyncio
from openai import AsyncOpenAI
import os

# import the key 
OPENAI_API_KEY = os.getenv("API_KEY")

# word input list
words = ["apple", "banana", "carrot", "date", "elephant", "fig", "grape", "horse", 
        "iguana", "jackfruit", "kiwi", "lemon", "mango", "nectarine", "orange", "peach"]

words2 = ['apple','banana','carrot','dog','elephant','flute','grape','hat','ice','jaguar',
          'kiwi','lion','mango','nectar','orange','pineapple']

async def get_grouped_words(words):
    # chatgpt prompt
    prompt = (
        f"Please group the following words into groups of 4 in a logical way to beat the game Connections:\n\n"
        f"{', '.join(words)}\n\n"
        "Provide the groups as lists of words."
    )

    # OpenAI client and request completion
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    completion = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a New York Times' Connections game expert."},
            {"role": "user", "content": prompt}
        ],
    )

    # return the result
    return completion.choices[0].message.content

async def main():
    grouped_words_output = await get_grouped_words(words)
    print("Grouped Words:\n", grouped_words_output)
    grouped_words_output = await get_grouped_words(words2)
    print("Grouped Words:\n", grouped_words_output)

if __name__ == "__main__":
    asyncio.run(main())
