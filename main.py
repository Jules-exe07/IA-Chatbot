import openai
from flask import jsonify
from flask import render_template
from views import views
from flask import Flask, request, render_template

app = Flask(__name__)
app.register_blueprint(views, url_prefix='/views')

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    # Get the user's message from the form submission
    message = request.form['message']

    # Send the message to the chatbot and get a response
    response = get_response_from_chatbot(message)

    # Return the response in JSON format
    return jsonify({'message': message, 'response': response})
  else:
    # Render the template without a chatbot response
    return render_template('index.html')

def get_response_from_chatbot(message):
  # Call the gpt3_completion function to get a response from the chatbot
  return gpt3_completion(message)



def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = open_file('openaiapikey.txt')


def gpt3_completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['Asistente:', 'Usuario: ']):
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['text'].strip()
    return text


if __name__ == '__main__':
    app.run(debug=True)
    conversation = list()
    while True:
        user_input = input('Usuario: ')
        conversation.append('Usuario: %s' % user_input)
        text_block = '\n'.join(conversation)
        prompt = open_file('prompt_chat.txt').replace('<<BLOCK>>', text_block)
        prompt = prompt + '\nAsistente'
        response = gpt3_completion(prompt)
        print('Asistente', response)
        conversation.append('Asistente: %s' % response)