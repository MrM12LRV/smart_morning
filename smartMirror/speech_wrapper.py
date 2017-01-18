# python3 -m pip install pocketsphinx

from speech_recognition import Microphone, Recognizer, AudioData

# TODO: get audio snippet when audio detected
def wait_for_audio():
    with Microphone() as audio_source:
        recognizer_instance = Recognizer()
        recognizer_instance.energy_threshold = 1000

        print("Spawning reader")
        audio_data = \
            recognizer_instance.listen_in_background( \
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

def read_microphone(duration = 5):
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