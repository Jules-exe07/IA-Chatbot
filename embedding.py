import openai
import numpy as np
from pprint import pprint


# Function to open a file and read its content
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


# Function to generate GPT-3 embeddings for a given text
def gpt3_embedding(content, engine='text-similarity-babbage-001'):
    content = content.encode(encoding='UTF-8', errors='replace').decode()
    response = openai.Embedding.create(input=content, engine=engine)
    vector = response['data'][0]['embedding']  # this is a normal list
    return vector


# Function to calculate the dot product (similarity) between two vectors
def similarity(v1, v2):
    return np.dot(v1, v2)


# Set OpenAI API key by reading it from a file
openai.api_key = open_file('openaiapikey.txt')


# Function to match a given vector to a list of pre-defined classes
def match_class(vector, classes):
    results = list()
    for c in classes:
        score = similarity(vector, c['vector'])
        info = {'category': c['category'], 'score': score}
        results.append(info)
    return results


if __name__ == '__main__':
    categories = ['']  # Add categories here
    classes = list()
    
    # Generate embeddings for each category and store them in a list
    for c in categories:
        vector = gpt3_embedding(c)
        info = {'category': c, 'vector': vector}
        classes.append(info)
    
    # Uncomment these lines to print the list of classes and exit the program
    # pprint(classes)
    # exit(0)
    
    # Start a loop to continually ask for user input and match it to pre-defined classes
    while True:
        a = input('Enter a lifeform here: ')
        vector = gpt3_embedding(a)
        result = match_class(vector, classes)
        pprint(result)
