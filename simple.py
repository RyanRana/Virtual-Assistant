import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import calendar
import random
import wikipedia

def recordAudio():

    r = sr.Recognizer()
    with sr.Microphone() as source:  
       print('Say something!')
       audio = r.listen(source)
    data = ''
    try:
        data = r.recognize_google(audio)
        print('You said: ' + data)
    except sr.UnknownValueError:
        print('Audio was not proccessed')
    except sr.RequestError as e:
        print('Request error found so audio was not proccessed')
    return data

def assistantResponse(text):
    print(text)

    myobj = gTTS(text=text, lang='en', slow=False)
    myobj.save('assistant_response.mp3')
    os.system('start assistant_response.mp3')

# A function to check for wake word(s)
def wakeWord(text):
    WAKE_WORDS = ['hey computer', 'okay computer'] 
    text = text.lower()
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    return False

def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day
    month_names = ['January', 'February', 'March', 'April', 'May',
       'June', 'July', 'August', 'September', 'October', 'November',   
       'December']
    ordinalNumbers = ['1', '2', '3', '4', '5', '6', 
                      '7', '8', '9', '10', '11', '12',                      
                      '13', '14', '15', '16', '17', 
                      '18', '19', '20', '21', '22', 
                      '23', '24', '25', '26', '27', 
                      '28', '29', '30', '31']
    return 'Today is ' + weekday + ' ' + month_names[monthNum - 1] + ', ' + ordinalNumbers[dayNum - 1] + '.'


def greeting(text):

    GREETING_INPUTS = ['hi', 'hey', 'hola', 'greetings', 'wassup', 'hello']
 
    GREETING_RESPONSES = ['howdy', 'whats good', 'hello', 'hey there']

    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + '.'

    return ''



def getPerson(text):
 wordList = text.split()
 for i in range(0, len(wordList)):
   if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i + 1].lower() == 'is':
            return wordList[i + 2] + ' ' + wordList[i + 3]

while True:

    text = recordAudio()
    response = ''
    if (wakeWord(text) == True):
         response = response + greeting(text)
         if ('date' in text):
             get_date = getDate()
             response = response + ' ' + get_date
         if('time' in text):
             now = datetime.datetime.now()
             meridiem = ''
             if now.hour >= 12:
                 meridiem = 'p.m'
                 hour = now.hour - 12
             else:
                 meridiem = 'a.m'
                 hour = now.hour
                 if now.minute < 10:
                     minute = '0'+str(now.minute)
                 else:
                     minute = str(now.minute)
             response = response + ' '+ 'It is '+ str(hour)+ ':'+minute+' '+meridiem+' .'
         if ('who is' in text):
             person = getPerson(text)
             wiki = wikipedia.summary(person, sentences=2)            
             response = response + ' ' + wiki
         assistantResponse(response)
