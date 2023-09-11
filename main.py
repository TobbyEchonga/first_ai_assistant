from datetime import datetime
import speech_recognition as sr
import logging.config as listen
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

# Speech engine initialization
engine = pyttsx3.init()
voices = engine.getProperty('voices')
#get the male voice which is 0 in the array 1 =female
engine.setProperty("voice", voices[0].id)
activationWord = 'mina' #single word

#Configure the browser to set
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path) )


#method for text to speech and rate is the speed of speech
def speak(text, rate = 120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

#listen to a command from microphone
def parseCommand():
    listener = sr.Recognizer()
    print('Listening for a command')

    #tapping into the microphone
    with sr.Microphone() as source:
        #pause threshold of 2 minutes
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    #input speech
    try:
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech, language='en_gb')
        print(f'The input speech was: {query}')
    except Exception as exception:
        print('I did not quite cath that')
        speak('I did not quite cath that')

        print(exception)
        return 'None'
    
    return query

#Search wikipedia
def search_wikipedia(query):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No wikipedia results')
        return 'No results received'
    try :
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary



#main loop
if __name__ == '__main__':
    speak('All Systems normal.')

    while True:
        #parse sentences a lists of words
        query = parseCommand().lower().split()
        if query[0] == activationWord:
            query.pop(0)

            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings, all')
                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speak)

            #navigate to website
            if query[0] == 'go' and query[1] == 'to':
                speak('Opening...')
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)

            #navigate to wikipedia
            if query[0] == 'search':
                query = ' '.join(query[1:])
                speak('Querying the universal database')
                speak(search_wikipedia(query))

            #navigate to take notes
            if query[0] == 'log':
                speak('Ready to record your notes')
                newNote = parseCommand().lower()
                now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                
                with open('note_%s.txt' % now,'w') as newFile:
                    newFile.write(newNote)
                speak('Note taken')

            if query[0] == 'exit':
                speak('GoodBye')
                break
                





