from flask import Flask, request
import requests
from twilio.rest import Client
import tempfile
import logging

from services import transcribe_api
from config import Config

sid = Config.TWILIO_SID
twilio_token = Config.TWILIO_TOKEN
twilio_num = Config.TWILIO_NUMBER
client = Client(sid, twilio_token)

def chunk_message(message: str, max_length: int = 1600):
    """
    Splits a message into chunks of a given max length without breaking words.
    
    Args:
        message (str): The message to be split.
        max_length (int): Maximum length of each chunk. Default is 1600 characters.
    
    Returns:
        list: A list of message chunks.
    """
    words = message.split()
    chunks = []
    current_chunk = []

    current_length = 0
    for word in words:
        # If adding this word would exceed the max length, finalize the current chunk
        if current_length + len(word) + 1 > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(word)
        current_length += len(word) + 1  # Account for the space after the word
    
    # Add the last chunk if there are remaining words
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def send_whatsapp_message(client, phone_number, text): # Send a whatsapp message with a Twilio
    message = client.messages.create(
        from_='whatsapp:{}'.format(twilio_num),
        body=text,
        to='whatsapp:{}'.format(phone_number)
        )
    print("message sent to: {}, sid: {}".format(phone_number,message.sid))


app = Flask(__name__)

# Webhook to receive WhatsApp audio

@app.route('/whatsapp', methods=['POST'])
def wa():
    # Strip relevant information from message
    data = request.form
    user_phone = data.get('From')
    if user_phone and user_phone.startswith('whatsapp:'):
        user_phone = user_phone[len('whatsapp:'):]
    print("Received request from ",user_phone)
    message_id = data.get('MessageSid') # Message UID from Twilio
    message_body = data.get('Body') # In case you want to fetch the body of the message
    num_media = int(data.get('NumMedia', 0))

    # First, transcribe the message as fast as possible. Do not check DB
    if num_media == 1:
        media_url = data.get('MediaUrl0')  # Get the URL of the media
        media_type = data.get('MediaContentType0')  # Get the media content type

        if media_type.startswith('audio/'):
            try:
                response = requests.get(media_url, auth=(sid, twilio_token)) # Use Twilio REST API to download the media file
                if response.status_code != 200:
                    raise Exception(f"Failed to download audio file. Status code: {response.status_code}")
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as temp_file: # Get media file and put it in a temp file
                    temp_file.write(response.content)
                    temp_path = temp_file.name
                message = transcribe_api(temp_path)

                if len(message) < 1600: #Chunk message logic
                    send_whatsapp_message(client, user_phone, message)
                else:
                    message_chunks = chunk_message(message)
                    for i, chunk in enumerate(message_chunks):
                        try:
                            send_whatsapp_message(client,user_phone,chunk)
                        except Exception as e:
                            logging.error(f"Error sending message {i+1}: {e}")
            except Exception as e:
                logging.error(f"Error transcribing message: {e}")

        else:
            message ="The file you sent does not look like an audio file"
            send_whatsapp_message(client, user_phone, message)

    else:
        message ="Please send an audio file"
        send_whatsapp_message(client, user_phone, message)

    return ('', 200) # Otherwise Twilio complains and throws error logs. Please note that if the runtime takes more than few seconds it will fail anyway

if __name__ == "__main__":
    app.run(port = 5002, debug=False) #Ready to deploy and test locally. Set ngrok to use the port 5002 as the default one might conflict. Use: ngrok http 5002
