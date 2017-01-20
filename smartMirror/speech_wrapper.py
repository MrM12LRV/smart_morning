# python3 -m pip install pocketsphinx

from speech_recognition import Microphone, Recognizer, AudioData
from requests import get
import json
from pprint import PrettyPrinter

class SpeechFunctioner():

    def __init__(self):
        self.prettyprinter = PrettyPrinter(indent=4)

        self.HIGH = 4000
        self.LOW = 1000
        self.SENSITIVITY = self.HIGH
        self.response_json = None
        self.voice_function = None


    def __async_listener_fn(self, recognizer_instance, audio_data):

        print("Performing Sphinx Speech to Text asynchronously")
        try:
            text_from_audio = \
                recognizer_instance.recognize_sphinx( \
                    audio_data, show_all = False)
        except Exception as e:
            print(
                "Exception in recognizer: " + str(e))
            text_from_audio = None

        print("Text recognized:\n\t", end="")
        print(text_from_audio)
        print("Sending HTTP request to API AI")
        self.response_json = \
            get('https://api.api.ai/v1/query?v=20150910&query=%s&lang=en&sessionId=1234567890' % text_from_audio,
                headers={
                    'language-tag'  : 'en',
                    'Authorization' : 'Bearer e4099166fd7a41218ba851d21e6866f5',
                    'Content-Type'  : 'application/json; charset=utf-8'
                }
            )

        print("Got structure back:")
        try: self.prettyprinter.pprint(self.response_json.json())
        except: print("Could not print JSON result.")

        try:
            self.voice_function = self.response_json.json()['result']['metadata']['intentName']
        except Exception as err:
            print("Not a valid voice function", self.voice_function)
            print("Exception: {0}".format(err))
            voice_function = None

        return text_from_audio

    # developer:    cac03a5b9aca49e2b63e97f7c0ae0cec    (managing entities and intents)
    # client:       e4099166fd7a41218ba851d21e6866f5    (making queries)
    # Authorization: Bearer YOUR_ACCESS_TOKEN

    def async_read_microphone(self):
        recognizer_instance = Recognizer()
        recognizer_instance.energy_threshold = self.SENSITIVITY
        recognizer_instance.phrase_time_limit = 20 # TODO: I don't think this variable is working
                                                   #       find out how to change phrase time limit.
                                                   #       Do we want this phrase time_limit?
        try: audio_source = Microphone()
        except OSError as oserr: print("OSError: {0}".format(oserr)); return

        print("Spawning reader")
        stop_listener_fn = \
            recognizer_instance.listen_in_background( \
                audio_source, self.__async_listener_fn)

        print("Leaving read microphone")
        """print("Waiting to read for 10 seconds")
        from time import sleep
        sleep(100)                  # TODO: when do we stop lisening?
        stop_listener_fn()          #       Probably never; Maybe when we
                                    #       just quit out of app?
        print("No longer taking audio input")
        
        return
        """


    def sync_read_microphone(self, duration = 3):
        with Microphone() as audio_source:
            recognizer_instance = Recognizer()
            recognizer_instance.energy_threshold = self.SENSITIVITY

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
            print("Sending HTTP request to API AI")

            self.response_json = \
                get('https://api.api.ai/v1/query?v=20150910&query=%s&lang=en&sessionId=1234567890' % text_from_audio,
                    headers={
                        'language-tag'  : 'en',
                        'Authorization' : 'Bearer e4099166fd7a41218ba851d21e6866f5',
                        'Content-Type'  : 'application/json; charset=utf-8'
                    }
                )

            print("Got structure back:")
            try: self.prettyprinter.pprint(self.response_json.json())
            except: print("Could not print JSON result.")

            try:
                self.voice_function = self.response_json.json()['result']['metadata']['intentName']
            except Exception as err:
                print("Not a valid voice function", self.voice_function)
                print("Exception: {0}".format(err))
                voice_function = None
            return text_from_audio
