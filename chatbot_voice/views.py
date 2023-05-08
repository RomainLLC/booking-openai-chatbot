# OpenAI based chatbot booking example
# Author : Romain Leclerc
# Original repo : https://github.com/RomainLLC/booking-openai-chatbot

from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse

import openai

openai.api_key = settings.OPENAI_API_KEY


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    # print(str(response.choices[0].message))
    return response.choices[0].message["content"]


context = [ {'role':'system', 'content':"""
You are AlIne, an automated appointment booking service for local gov. \
The user can book a slot for creation or renewal of passport or identity card.
You wait to collect the entire booking, then summarize it and check for a final \
time if the customer is ok with the slot provided. \
You first greet the customer, then collects the booking wishes, \
and then asks if it's for a passport or identity card. \
If it's a passport or id card, you ask if it's a creation or renewal, then \
 you give the available dates and slots as a n html list and aks user which slot he wants to book. \
You respond in a short, very conversational friendly style. \
Finally you collect the user first name, last name, and phone number. \
Make sure to clarify all booking options, dates, available slots to uniquely \
identify the items from the agenda. \
Agenda contains dates formated as dd/MM HH:mm and a number for available slots. \
When a user books a slot, deduce 1 to the corresponding date remaining available slots. Zero slots means no booking possible at that date. \
Answer in user's language as concisely as possible. Users are french. Knowledge cutoff: Nov 2021 Current date: 7 May 2023. \
In your answers, you must allways output numbers in full text string, example: "5" output is "five". 
You must output agenda dates in full text string, example: "25/05 11:00" must output as "twenty-five may at eleven hour". \
The agenda includes \
25/05 11:00    2 \
30/05 09:00    1 \
02/06 10:00    1 \
"""} ]  # accumulate messages

messages =  context.copy()

from TTS.api import TTS
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

import io

from django.conf import settings as django_settings
import os

import site

location = site.getsitepackages()[0]

path = location+"/TTS/.models.json"

model_manager = ModelManager(path)

model_path, config_path, model_item = model_manager.download_model("tts_models/fr/mai/tacotron2-DDC")

voc_path, voc_config_path, _ = model_manager.download_model(model_item["default_vocoder"])


synthesizer = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    vocoder_checkpoint=voc_path,
    vocoder_config=voc_config_path,
    use_cuda=True
)

def get_voice_from_text(text):
    outputs = synthesizer.tts(text)
    filename = 'answer.wav'
    dir = settings.MEDIA_ROOT
    synthesizer.save_wav(outputs, str(dir) + '/' + filename)
    return filename

def index(request):
    result = ''
    voice = ''
    if request.method == "POST":
        print(str(request.POST.get('csrfmiddlewaretoken')))
        message = request.POST.get('demande')
        context.append({'role':'user', 'content':f"{message}"})

        result = get_completion_from_messages(context, temperature=0.6)
        context.append({'role':'assistant', 'content':f"{result}"})
        voice = get_voice_from_text(result)

    return render(request, 'chatbot_voice/index.html', {'result': result, 'voice': str(settings.MEDIA_URL) + "/" + voice })



