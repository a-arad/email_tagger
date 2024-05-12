import os
import openai
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

def get_completion(prompt, model="gpt-4"):
    '''basic completion from gpt4'''
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    return response.choices[0].message["content"]