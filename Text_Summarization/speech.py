import os
import speech_recognition as sr
import webbrowser
from datetime import datetime

r = sr.Recognizer()

audio_spoken = ''
with sr.Microphone() as source:
    while audio_spoken != 'stop':
        print("Say Something")
        os.system("""osascript -e 'display notification "{}" with title "{}"'""".format("Title", "Say Something"))
        audio = r.listen(source)
        print('Time over')
        os.system("""osascript -e 'display notification "{}" with title "{}"'""".format("Title", "Time Over"))

        try:
            audio_spoken = r.recognize_google(audio)
            f = open('blog.txt', 'a')
            f.write('\n\n')
            f.write(str(datetime.now()))
            f.write('\n')
            f.write(audio_spoken)
            f.close()
        except:
            pass