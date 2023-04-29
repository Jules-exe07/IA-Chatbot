import openai


# Function to open a file and read its content
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


# Set OpenAI API key by reading it from a file
openai.api_key = open_file('openaiapikey.txt')


# Function to generate GPT-3 completions given a prompt
def gpt3_completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['Asistente:', 'Usuario:']):
    # Encode prompt to UTF-8 and replace any errors
    prompt = prompt.encode(encoding='UTF-8', errors='replace').decode()
    
    # Call OpenAI's Completion API with the specified parameters
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    
    # Extract the generated text from the API response
    text = response['choices'][0]['text'].strip()
    
    return text


# Main function to run a chatbot interaction with the user
if __name__ == '__main__':
    conversation = list()
    
    # Start a loop to continually ask for user input and generate responses
    while True:
        user_input = input('Usuario: ')
        conversation.append('Usuario: %s' % user_input)
        text_block = '\n'.join(conversation)
        
        # Read the chat prompt from a file and substitute the conversation block
        prompt = open_file('prompt_chat.txt').replace('<<BLOCK>>', text_block)
        prompt = prompt + '\nAsistente:'
        
        # Call the GPT-3 function to generate a response given the prompt
        response = gpt3_completion(prompt)
        print('Asistente:', response)
        
        # Add the generated response to the conversation history
        conversation.append('Asistente: %s' % response)
