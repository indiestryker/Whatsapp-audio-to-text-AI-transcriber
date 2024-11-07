# import whisper
from pydub import AudioSegment
from openai import OpenAI

from config import Config


def transcribe_api(path):
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    audio_file= open(path, "rb")
    transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return(transcription.text)

### In case you need to get the duration of the audio
def get_audio_duration(path):
    try:
        audio = AudioSegment.from_file(path, format="ogg")
        duration_in_seconds = len(audio) / 1000
        return duration_in_seconds
    except Exception as e:
        raise Exception(f"An error occurred while processing the audio file: {e}")
    
### If you want to host your own whisper model, use the function below instead of transcribe_api. 
### Tip: the API is very cheap and the model is very fat. It's definitelyworth the money

# def transcribe(path, model_name="base"): 
#     try:
#         model = whisper.load_model(model_name)
#         print('transcription in progress')
#         result = model.transcribe(path)
#         print('transcription completed')
#         return result["text"]
#     except Exception as e:
#         raise Exception(f"An error occurred during the whispering: {e}")