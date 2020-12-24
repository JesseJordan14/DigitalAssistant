import time
import speech_recognition as sr
import os
from gtts import gTTS
from datetime import datetime
import warnings
import calendar
import random
import wikipedia
from playsound import playsound
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
import shutil
import mysql.connector as mysql
from mysql.connector import connection

warnings.filterwarnings('ignore')


# Record audio and return as string
def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something: ')
        audio = r.listen(source)
        data = ''

        try:
            data = r.recognize_google(audio)
            print('You said: ' + data)
        except sr.UnknownValueError:
            print('Google speech recognition could not understand the input audio')
        except sr.RequestError as e:
            print('Google speech recognition error: ' + str(e))

    if 'vulcan' in data.lower():    # if recognized as a command for Vulcan. TODO: implement using nicknames as hotwords
        return data                 # return recorded text
    else:
        return 'NO_RESPONSE'


def assistant_respond(phrase):
    print(phrase)

    speak = gTTS(text=phrase, lang='en', slow=False)

    speak.save('assistant_response.mp3')
    playsound('assistant_response.mp3')
    if os.path.exists("assistant_response.mp3"):
        delete_file("assistant_response.mp3")
    else:
        print("The file does not exist")


async def delete_file(file):
    os.remove(file)


def create_response(user_input):
    if user_input == '':
        return ' '
    if 'vulcan' in user_input:
        user_input = user_input.replace('vulcan ', '')  # remove "vulcan" from input
    print('user input: ' + user_input)
    if user_input.find('play') == 0:
        play_song(user_input.replace('play ', ''))
        # download_youtube_audio(user_input.replace('youtube ', ''))
    if user_input == 'how are you today':
        return 'I am well'
    if user_input.lower() == 'what is your name':
        return 'My name is Vulcan'
    if user_input == 'what is the time':
        hour = datetime.now().hour
        minute = datetime.now().minute
        minute_str = ''
        day_half = ''
        if 10 > minute > 0:
            minute_str = 'O ' + str(minute)
        if minute == 0:
            minute_str = "O'clock "
        else:
            minute_str = str(minute)
        if hour > 12:
            day_half = 'P.M.'
            hour = hour - 12
        else:
            day_half = 'A.M'
            if hour == 0:
                hour = 12
        return 'it is ' + str(hour) + ' ' + minute_str + day_half


def start_listening():
    while True:
        text = record_audio()
        if text == 'NO_RESPONSE':
            return
        assistant_text = create_response(text.lower())
        # assistant_respond(assistant_text)


def play_song(search_text):
    file_name = song_already_downloaded(search_text)
    if file_name == '':
        download_youtube_audio(search_text)
    else:
        os.system("start " + file_name)


def song_already_downloaded(title):
    title_array = title.lower().split()
    length = len(title_array)
    for file in os.listdir("C:\\Users\\16jjo\\Jesse\\Droid\\Music"):
        for word in title_array:
            if word not in file.title().lower():
                break
            if word == title_array[len(title_array) - 1] and word in file.title().lower():
                return "C:\\Users\\16jjo\\Jesse\\Droid\\Music\\" + file.title()
    return ''


def download_youtube_audio(search_text):    # find first result on youtube with given search string, download mp3
    search_text.replace(' ', '+')           # replace spaces with +'s in search string
    driver = webdriver.Chrome('C:/Drivers/chromedriver_win32/chromedriver')     # driver for scraping the web
    wait = WebDriverWait(driver, 10)
    # driver = webdriver.Chrome()
    url = 'https://www.youtube.com/results?search_query=' + search_text + ' lyrics'
    driver.get(url)                                                             # go to search result page of youtube
    download_link = driver.find_element_by_xpath('//*[@id="contents"]/ytd-video-renderer[1]')\
        .find_element_by_xpath('//*[@id="video-title"]').get_attribute('href')  # get link of first video

    driver.get('https://ytmp3.cc/en13/')
    driver.find_element_by_xpath('//*[@id="input"]').send_keys(download_link)
    driver.find_element_by_xpath('//*[@id="submit"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="buttons"]/a[1]').click()
    time.sleep(5)
    driver.close()
    for file in os.listdir("C:\\Users\\16jjo\\Downloads"):
        if file.endswith(".mp3"):
            # move file to separate directory
            filename = file.title()
            os.rename("C:\\Users\\16jjo\\Downloads\\" + filename, "C:\\Users\\16jjo\\Downloads\\"
                      + file.title().replace(" ", ""))
            filename = filename.replace(" ", "")
            shutil.move("C:\\Users\\16jjo\\Downloads\\" + filename,
                        "C:\\Users\\16jjo\\Jesse\\Droid\\Music\\" + filename)
            time.sleep(5)
            os.system("start C:\\Users\\16jjo\\Jesse\\Droid\\Music\\" + filename)
            break


def connect_db():
    db_connection = connection.MySQLConnection(host="10.0.0.102", database="exampledb", user="exampleuser", password="pimylifeup")
    #db_connection = mysql.connect(host="172.20.10.10", database="exampledb", user="jesselaptop", password="1mHungry")
    print("Connected to: " + db_connection.get_server_info())
    

connect_db()
# start_listening()
# create_response(text)
# assistant_respond(create_response(text))
