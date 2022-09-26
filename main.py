from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts 
import sys 

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ['go shopping groceries', 'pay credit card', 'roast coffee']

def create_note():
	global recognizer
	speaker.say("what do you want to write in your note?")
	speaker.runAndWait()

	done = False

	while not done:
		try: 
			with speech_recognition.Microphone() as mic:
				recognizer.adjust_for_ambient_noise(mic, duration=0.2)
				audio = recognizer.listen(mic)

				note = recognizer.recognize_google(audio)
				note = note.lower()

				speaker.say("choose a file name")
				speaker.runAndWait()

				recognizer.adjust_for_ambient_noise(mic, duration=0.2)
				audio = recognizer.listen(mic)

				filename = recognizer.recognize_google(audio)
				filename = filename.lower()

			with open(filename, 'w') as f:
				f.write(note)
				done = True 
				speaker.say(f"your note has been created {filename}")
				speaker.runAndWait()

		except speach_recognition.UnknownValueError:
			recognizer = speech_recognition.Recognizer()
			speaker.say("i did understand your request")
			speaker.runAndWait()


def add_todo():
	global recognizer 

	speaker.say("what todo do you want to add?")
	speaker.runAndWait()
	done = False 

	while not done:
		try:
			with speech_recognition.Microphone() as mic:
				recognizer.adjust_for_ambient_noise(mic, duration=0.2)
				audio = recognizer.listen(mic)
				item = recognizer.recognize_google(audio)
				item = item.lower()
				todo_list.append(item)
				done = True

				speaker.say(f"i added {item} to your list")
				speaker.runAndWait()
		except speech_recognition.UnknownValueError:
			recognizer = speech_recognition.Recognizer()
			speaker.say("i did not understand. What was that again?")
			speaker.runAndWait()


def show_todos():
	speaker.say("the items on yout list")
	for item in todo_list:
		speaker.say(item)
	speaker.runAndWait()

def hello():
	speaker.say("hello ivonne, how can i help you?")
	speaker.runAndWait()

def exit():
	speaker.say("bye ivonne")
	speaker.runAndWait()
	sys.exit(0)

mappings = {
	"greetings": hello,
	"create_note": create_note,
	"add_todo": add_todo,
	"show_todos": show_todos,
	"exit": quit
}

asssintat = GenericAssistant('intents.json', intent_methods=mappings)
asssintat.train_model()

while True:
	try: 
		with speech_recognition.Microphone() as mic:
			recognizer.adjust_for_ambient_noise(mic, duration=0.2)
			audio = recognizer.listen(mic)

			message = recognizer.recognize_google(audio)
			message = message.lower()


		asssintat.request(message)
	except speech_recognition.UnknownValueError:
		recognizer = speech_recognition.Recognizer()

