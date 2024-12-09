# Transcribe whatsapp audio to text - full backend app

A Flask backend that can transcribe whatsapp audios into text using OpenAI Whisper model.

I host a version with my whatsapp bot already live. It's fully free, donation-based! Link [HERE](https://en.transcribe-bot.com/)

### Features, aka why it is special ❤️
- The backend app is ready to be used with error handling and fallback. You can start with just a production Twilio number. It has only one straightforward POST API endpoint.
- The repo is ready to be deployed in a server/docker/cloud and it is set up for high availability and scalability. It comes with a yaml file compatible with GCP, to be deployed with app engine. From test to live in 5 mins!
- The code supports inbound and outbound messaging from Twilio
- The Flask app is ready to support a database. Tested with GCP SQL cloud (watch out, use the socket option) and CockroachDB
- You can both use the API of Whisper, or host the model yourself. Just uncomment the function in services.py


_The code comes as an extended, maintained and ready to deploy version of [Paratustra's bot](https://github.com/paratustra/audio-transcription-bot/tree/main)_

## 1) Requirements
- openai-whisper
- python-dotenv
- twilio
- datetime
- openai
- pydub
- flask
- gunicorn

## 2) Setup
1. Clone this repository and navigate to the project directory.
2. Create and activate a new virtual environment (e.g. venv: `python3 -m venv venv` and `source venv/bin/activate`)
3. Install the required packages using pip: `pip install -r requirements.txt`
4. Get a Twilio number. If you do not have it already, it might take 2/3 days to be approved and have a production number and set it up (Under messaging / sendes / whatsapp senders). Meanwhile, you can test with their sandbox (messaging / try it out / send a whatsapp message)
5. Create an .env file in your repo with the following env variables:
    TWILIO_SID
    TWILIO_TOKEN
    TWILIO_NUMBER
    OPEN_API_KEY
    (optional) DB_URL

## 3) Testing (local)
You can first test locally. I suggest using [ngrok](https://github.com/NGROK) with its free version to test and debug locally:
1. Install ngrok `pip install ngrok` and register your account
2. Run the file __init__.py `python3 __init.py`
3. Create a server forwarding (the free version works great) by running `ngrok http 5002`
4. Copy-paste the the forwarding link into the Twilio webhook field. It looks like <some_numbers>.ngrok-free.app . Add the path to your endpoint (e.g. <some_numbers>.ngrok-free.app/whatsapp).
5. Send a audio message to your Twilio number

## 4) Deploy to GCP or with any docker server
I set up gunicorn to be able to handle multiple requests elegantly. You will be able to handle thousands of message per minute!

- If you use GCP: Just update the environmental variable with the ones specified above (setup step #5) and use the gcloud CLI suite to deploy to your tenant. No need to dockerize, App Engine is quite lightweight
- If you use docker: adapt the yaml file and use gunicorn as runtime

# License
This project is licensed under the MIT License - see the LICENSE.md file for details.
