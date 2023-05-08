# Booking chatbot web app with OpenAI API, Django and Coqui TTS

This is an example app to experiment a chatbot creation with OpenAI API

demo-openai-chatbot-text-to-speech-web.mp4

# Requirements

- Basic Pyhton knowledge : setting up a virtualenv and install python3
- An OpenAPI key

# Packages

python -m pip install Django
pip install wheel openai python-dotenv pillow django-feather TTS gruut-lang-fr

# Notes

- Configured and tested with GPT-3.5
- Prompt is in english, as in native language it provided weird outputs, mixing languages
- For text to speech, free version of Coqui TTS package is used (no API key). 