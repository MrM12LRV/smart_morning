# python3 -m pip install pocketsphinx

from speech_recognition import Microphone, Recognizer, AudioData
from requests import get
import json

def asynch_listener_fn(recognizer_instance, audio_data):
    print("Performing Sphinx Speech to Text asynchronously")
    try:
        text_from_audio = \
            recognizer_instance.recognize_sphinx( \
                audio_data, show_all = False)
    except Exception as e:
        print(
            "Exception in recognizer: " + str(e))
        text_from_audio = None

    print(text_from_audio)

    # TODO: send this text to Alina's API.AI using a GET request
    some_structure = \
        requests.get('http://api.aidomainnameWHATisTHIS/somemethod?query=%s' % text_from_audio)
    some_structure.json() # is this a json?
    return text_from_audio

def async_read_microphone():
    recognizer_instance = Recognizer()
    recognizer_instance.energy_threshold = 1000 # TODO: modify sensitivity
    recognizer_instance.phrase_time_limit = 20 # TODO: I don't think this variable is working
                                               #       find out how to change phrase time limit.
                                               #       Do we want this phrase time_limit?
    audio_source = Microphone()
    print("Spawning reader")
    stop_listener_fn = \
        recognizer_instance.listen_in_background( \
            audio_source, asynch_listener_fn)

    print("Waiting to read for 10 seconds")
    from time import sleep
    sleep(100)                  # TODO: when do we stop lisening?
    stop_listener_fn()          #       Probably never; Maybe when we
                                #       just quit out of app?
    print("No longer taking audio input")
    
    return


def sync_read_microphone(duration = 5):
    with Microphone() as audio_source:
        recognizer_instance = Recognizer()
        recognizer_instance.energy_threshold = 1000

        print("Reading")
        audio_data = \
            recognizer_instance.record( \
                audio_source, duration = duration)

        print("Performing Sphinx Speech to Text")
        try:
            text_from_audio = \
                recognizer_instance.recognize_sphinx( \
                    audio_data, show_all = False)
        except Exception as e:
            print(
                "Exception in recognizer: " + str(e))
            text_from_audio = None

        print(text_from_audio)
        return text_from_audio
    return None