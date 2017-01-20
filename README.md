# Smart Morning
Smart Mirror - displays important information and reminders for your day - such as weather, schedule,etc - on your own mirror! Smart Coffee Mug - using RF technology, the LED's on a coffee mug will light up to notify you if your coffee is too hot or cold when you bring your hand near it!

# Smart Mug

TODO: info about smart mug / how it works / how the code is organized

# Smart Mirror

TODO: info about smart mirror / how it works / how the code is organized

# Links
http://build18.herokuapp.com/garage/project/236/

# Installation

TODO: put other requirements... we may have missed some

On Mac

For speech to text:

    python3 -m pip install pocketsphinx
    brew install portaudio // required by PyAudio
    python3 -m pip install PyAudio
    python3 -m pip install SpeechRecognition

Some libraries for smart mirror:

    python3 -m pip install lxml
    python3 -m pip install requests
    python3 -m pip install pillow       // PIL image library

On Linux

For speech to text:

    sudo apt-get update
    sudo apt-get install libpulse-dev // needed by pocketsphinx
    brew install portaudio
    python3 -m pip install PyAudio
    python3 -m pip install SpeechRecognition

Some libraries for smart mirror:

    python3 -m pip install lxml
    python3 -m pip install requests
    python3 -m pip install pillow       // PIL image library
