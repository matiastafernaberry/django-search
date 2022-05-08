import gtts
from playsound import playsound

# make request to google to get synthesis
tts = gtts.gTTS("hola", lang="es")
tts.save("hello.mp3")
playsound("hello.mp3")