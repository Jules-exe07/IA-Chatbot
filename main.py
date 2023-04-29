import openai
from flask import jsonify, render_template, Flask, request
from views import views

# Initialize Flask app and register blueprints
app = Flask(__name__)
app.register_blueprint(views, url_prefix='/views')

# Define the main route of the app
@app.route('/', methods=['GET', 'POST'])
def index():
    # Function to handle user input and get a response from the chatbot
    def get_response_from_chatbot(message):
        # Call the gpt3_completion function to get a response from the chatbot
        return gpt3_completion(message)

    # Render the index.html template
    return render_template('index.html')

# Function to open and read a file
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Set OpenAI API key from file
openai.api_key = open_file('openaiapikey.txt')

# Function to get a response from OpenAI's GPT-3 model
def gpt3_completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['Asistente:', 'Usuario: ']):
    # Encode prompt as ASCII to remove non-ASCII characters
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    # Call OpenAI's GPT-3 API to get a response
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    # Extract the text from the response and strip any whitespace
    text = response['choices'][0]['text'].strip()
    return text

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
    # Initialize conversation history list
    conversation = list()
    while True:
        # Prompt the user for input and append it to the conversation history list
        user_input = input('Usuario: ')
        conversation.append('Usuario: %s' % user_input)
        # Combine the conversation history into a single text block and replace <<BLOCK>> in the prompt file
        text_block = '\n'.join(conversation)
        prompt = open_file('prompt_chat.txt').replace('<<BLOCK>>', text_block)
        # Add a prompt for the chatbot and get a response from OpenAI's GPT-3 model
        prompt = prompt + '\nAsistente'
        response = gpt3_completion(prompt)
        # Print the chatbot's response and append it to the conversation history list
        print('Asistente', response)
        conversation.append('Asistente: %s' % response)
