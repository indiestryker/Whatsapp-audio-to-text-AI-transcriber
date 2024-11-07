from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    TWILIO_SID = os.getenv('TWILIO_SID')
    TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
    TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
    OPENAI_API_KEY = os.getenv('OPEN_API_KEY')
    DB_URL = os.getenv('DB_URL')