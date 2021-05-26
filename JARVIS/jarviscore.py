import datetime
# import os
import json
import sys
import time
import PyPDF2
import instaloader
# GUI
import playsound
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QTime, QTimer, QDate, Qt
# from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from PyQt5.uic import loadUiType
from jarvisgui import Ui_MainWindow
#######
# import re
from JARVIS.closeModule import stop
import subprocess
import requests
import random
import wikipedia
import webbrowser
from vlc import MediaPlayer
from threading import Thread
from JARVIS.classesAndModule import Alarm, sendMail, News, playlist, Wtsp
from JARVIS.jarvisVoice import JarvisSpeak as j
# import speech_recognition as sr
from JARVIS.speechRecog import speechRecog
import pyautogui
import pywhatkit as kit

# brain gui
# from contextlib import redirect_stdout
import io

###############

old_cmd = ""
nameInt = 0

url = "http://api.openweathermap.org/data/2.5/weather?q=bhopal&appid=ef831cc525f939c8eb6824aa48c69c82"
weather = requests.get(url).json()
arts = weather["weather"][0]["main"]
temperature = weather["main"]["temp"]
humidity = weather["main"]["humidity"]


def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour <= 12:
        j.speak("Good Morning ,How can i help you Sir")
    elif hour == 12:
        j.speak("Good Noon ,How can i help you Sir")
    elif 12 <= hour < 18:
        j.speak("Good After Noon ,How can i help you Sir")
    else:
        j.speak("Good Evening ,How can i help you Sir")


def store(cmd):
    global old_cmd
    if cmd != "again":
        old_cmd = cmd  # if i == 0 else brain(old_cmd)
    else:
        pass
    return 0


# def take_command():
#     j.speak("listening")
#     while True:
#         try:
#             # print(1/0)
#             r = sr.Recognizer()
#             with sr.Microphone() as source2:
#                 r.pause_threshold = 1
#                 r.adjust_for_ambient_noise(source2)  # , duration=0.2
#                 print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tRecognizing.....")
#                 audio2 = r.listen(source2, phrase_time_limit=5)
#                 usr_command = r.recognize_google(audio2, language="en-in")
#                 usr_command = usr_command.lower()
#                 print(
#                     "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tyou said ->" + usr_command)
#                 return usr_command
#         except sr.UnknownValueError:
#             print("try Again")
# def take_command():
#     try:
#         usr_command = input("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tcommand :")
#         print("You said : "+usr_command)
#         return usr_command
#     except Exception as ex:
#         print(ex)
#         return 0
global usr_obj, f


class MainThread(Thread):
    global usr_obj, f

    # def __init__(self):
    #     super(MainThread, self).__init__()

    def run(self):
        wish_me()
        terminate = 0
        global f
        f = io.StringIO()  # in-memory string buffer

        while terminate < 1:
            usr_obj = speechRecog()
            usr_command = usr_obj.take_command()
            # with redirect_stdout(f):
            # everything printed in here will go to f
            terminate = brain(usr_command)


def brain(usr_command):
    # print("brain of jarvis")
    global usr_obj

    try:
        ###################################                 COMMAND :   SEARCH
        if "search" in usr_command:
            if "youtube" in usr_command:
                j.speak("Searching...")
                usr_command = usr_command.replace("search", "")
                usr_command = usr_command.replace("youtube", "")

                class t8(Thread):
                    def run(self):
                        webbrowser.open(
                            "https://www.youtube.com/results?search_query=" + usr_command)

                o8 = t8()
                o8.start()
                return 0
            elif "google" in usr_command:
                j.speak("Searching...")
                usr = usr_command.replace("search", "")
                usr = usr.replace("google", "")

                class Thread1(Thread):
                    def run(self):
                        webbrowser.open(
                            "https://google.com/?#q=" + usr_command)
                        # stop.chrome(ch,1)

                o1 = Thread1()
                o1.start()
                return 0
            else:
                j.speak("what I want to search")
                # add = "search "
                # usr_command = speechRecog.take_command(self=None)
                # usr_command = str(usr_command) + add
                # brain()
                return 0
        ###################################                 COMMAND :   TODAY
        elif "today" in usr_command:
            if "day" in usr_command:
                j.speak("Today is " + datetime.datetime.now().strftime("%A"))
                return 0
            elif "time" in usr_command:
                j.speak(
                    "The time is " + str(datetime.datetime.now().strftime("%H hour and %M minutes")))
                return 0
            elif "date" in usr_command:
                j.speak("Today is " +
                        datetime.datetime.now().strftime("%d %B %Y"))
                return 0
            elif "News" in usr_command:
                News.news_of(5)
                return 0
        ###################################                 COMMAND :   PLAY
        elif "play" in usr_command:
            if usr_command.find("online") >= 0:
                j.speak("Searching...")
                usr = usr_command.replace("play", "")
                usr = usr.replace("online", "")

                class Thread7(Thread):
                    def run(self):
                        webbrowser.open(
                            "https://open.spotify.com/search/" + usr_command)

                o7 = Thread7()
                o7.start()
                return 0
            elif usr_command.find("youtube") >= 0:
                j.speak("Playing music...")
                usr = usr_command.replace("play", "")
                usr = usr.replace("music", "")
                usr = usr.replace("youtube", "")

                class Thread17(Thread):
                    def run(self):
                        kit.playonyt(usr)

                o17 = Thread17()
                o17.start()
                return 0
            elif usr_command.find("iron man") >= 0:
                print("Playing...")
                soundm = MediaPlayer(
                    "/media/aman/Disk/movie/Iron Man (2008) 720p.x264 BRrip Hindi by amit6688.mkv")
                soundm.play()
                return 0
            elif "song" in usr_command or "music" in usr_command or "stop playing" in usr_command:
                # try:
                if "stop" in usr_command:
                    stop.stopPlaylist(cal=None, i=2)
                else:
                    j.speak("how many song you want to listen")
                    song_number = int(
                        input("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tEnter value : "))
                    playlist.playlist(
                        "/home/aman/Music/*.mp3", song_number)
                # except:
                #     print(Exception)
                #     usr_command = usr_command.replace("play", "")
                #     usr_command = usr_command.replace("song", "")
                #     webbrowser.open("https://open.spotify.com/search/"+usr_command)
                return 0

            elif "playlist" in usr_command:
                print("Playing...")
                playlist.playlist(
                    ipath="/home/aman/Music/*.mp3", ival=None)

                return 0
            else:
                j.speak("can't " + usr_command)
                return 0
        ###################################                 COMMAND :   CLOSE
        elif "close" in usr_command:
            # try:
            if "calculator" in usr_command:
                stop.calculator(cal=None, i=2)
                return 0
            elif "calendar" in usr_command:
                stop.calendar(cal=None, i=2)
                return 0
            elif "terminal" in usr_command:
                stop.terminal(cal=None, i=2)
                return 0
            elif "libreoffice" in usr_command:
                stop.office(cal=None, i=2)
                return 0
            elif "netbeans" in usr_command:
                stop.netbeans(cal=None, i=2)
                return 0
            elif "chrome" in usr_command or "google" in usr_command:
                stop.chrome(cal=None, i=2)
                return 0
            elif "system monitor" in usr_command:
                stop.monitor(cal=None, i=2)
                return 0
            elif "pycharm" in usr_command:
                stop.pycharm(cal=None, i=2)
                return 0
            elif "vscode" in usr_command or "vs code" in usr_command:
                stop.vscode(cal=None, i=2)
                return 0
            elif "firefox" in usr_command or "mozilla" in usr_command:
                stop.firfox(cal=None, i=2)
                return 0
            elif "skype" in usr_command:
                stop.skype(cal=None, i=2)
                return 0
            elif "telegram" in usr_command:
                stop.telegram(cal=None, i=2)
                return 0
            elif "gedit" in usr_command or "text editor" in usr_command:
                stop.gedit(cal=None, i=2)
                return 0
            else:
                j.speak("what I wan't to close")
                add = "close "
                usr_command = usr_obj.take_command()
                usr_command = (str(usr_command) + add)
                brain(usr_command)
                return 0
        # except Exception:
        #     print(Exception)
        # return 0
        ###################################                 COMMAND :   OPEN
        elif "open" in usr_command:
            if "calculator" in usr_command >= 0:
                j.speak("Opening Calculator...")

                class Thread4(Thread):
                    def run(self):
                        cal = subprocess.Popen("gnome-calculator")
                        stop.calculator(cal=cal, i=1)

                o4 = Thread4()
                o4.start()
                return 0

            elif usr_command.find("calendar") >= 0:
                j.speak("Opening calendar...")

                class Thread18(Thread):
                    def run(self):
                        cal = subprocess.Popen("gnome-calendar")
                        stop.calendar(cal, 1)

                o18 = Thread18()
                o18.start()
                return 0
            elif "libreoffice" in usr_command or "text writer" in usr_command:
                j.speak("Opening Libreoffice ...")

                class Thread12(Thread):
                    def run(self):
                        lbr = subprocess.Popen(
                            "/usr/lib/libreoffice/program/soffice")
                        stop.office(lbr, 1)

                o12 = Thread12()
                o12.start()
                return 0
            elif "telegram" in usr_command:
                j.speak("Opening telegram ...")

                class Thread13(Thread):
                    def run(self):
                        tele = subprocess.Popen("/opt/telegram/Telegram")
                        stop.telegram(tele, 1)

                o13 = Thread13()
                o13.start()
                return 0
            elif "skype" in usr_command:
                j.speak("Opening skype ...")

                class Thread14(Thread):
                    def run(self):
                        sky = subprocess.Popen(
                            "/snap/skype/161/usr/share/skypeforlinux/skypeforlinux")
                        stop.skype(sky, 1)

                o14 = Thread14()
                o14.start()
                return 0
            elif usr_command.find("pycharm") >= 0:
                j.speak("Opening Pycharm...")
                pycharm = subprocess.Popen(
                    "/snap/pycharm-community/222/bin/pycharm.sh")
                stop.pycharm(pycharm, 1)
                return 0

            # elif "download" in usr_command:
            #     j.speak("Opening Downloads...")
            #     return 0
            #     down = subprocess.Popen("/home/aman/Downloads/")

            elif usr_command.find("netbeans") >= 0:
                j.speak("Opening Netbeans...")

                class Thread10(Thread):
                    def run(self):
                        net = subprocess.Popen(
                            "/usr/local/netbeans-8.2/bin/netbeans")
                        stop.netbeans(net, 1)

                o10 = Thread10()
                o10.start()
                return 0
            elif usr_command.find("youtube") >= 0 and usr_command.find("music") >= 0:
                j.speak("Playing music...")
                usr = usr_command.replace("play", "")
                usr = usr.replace("music", "")
                usr = usr.replace("youtube", "")

                class Thread17(Thread):
                    def run(self):
                        webbrowser.open(
                            "https://music.youtube.com/search?q=" + usr)

                o17 = Thread17()
                o17.start()
                return 0
            elif usr_command.find("google") >= 0 or usr_command.find("chrome") >= 0:
                j.speak("Opening google chrome...")

                class Thread3(Thread):
                    def run(self):
                        g = subprocess.Popen("/usr/bin/google-chrome")
                        stop.chrome(g, 1)

                o3 = Thread3()
                o3.start()
                return 0

            elif "youtube" in usr_command:
                j.speak("Opening youtube...")

                class Thread6(Thread):
                    def run(self):
                        webbrowser.open("https://youtube.com/#search")

                o6 = Thread6()
                o6.start()
                return 0
            elif "vs" in usr_command or "code" in usr_command:
                j.speak("Opening VisualStudio code...")

                class Thread11(Thread):
                    def run(self):
                        vs = subprocess.Popen("/usr/bin/code")
                        stop.vscode(vs, 1)

                o11 = Thread11()
                o11.start()
                return 0
            elif usr_command.find("instagram") >= 0 or usr_command.find("insta") >= 0:
                j.speak("Sir Please enter User name correctly :")
                name = input()

                j.speak("Sir this is Your Profile")

                class Thread18(Thread):
                    def run(self):
                        webbrowser.open(f"www.instagram.com/{name}")
                        # stop.chrome(g, 1)

                o18 = Thread18()
                o18.start()
                j.speak("Sir would you like to download the profile picture")
                cmd = usr_obj.take_command()
                if cmd == "yes":
                    mod = instaloader.Instaloader()
                    mod.download_profile(name, profile_pic_only=True)
                    j.speak(
                        "Profile pic is downloaded in your default folder")
                else:
                    j.speak("Ok sir")
                return 0
            elif "firefox" in usr_command or "mozilla" in usr_command:
                j.speak("Opening mozilla firefox ...")

                class Thread15(Thread):
                    def run(self):
                        fir = subprocess.Popen("/usr/bin/firefox")
                        stop.firfox(fir, 1)

                o15 = Thread15()
                o15.start()
                return 0
            elif "gedit" in usr_command or "text editor" in usr_command:
                j.speak("Opening gedit text editor ...")

                class Thread16(Thread):
                    def run(self):
                        edit = subprocess.Popen("/usr/bin/gedit")
                        stop.gedit(edit, 1)

                o16 = Thread16()
                o16.start()
                return 0

            elif usr_command.find("terminal") >= 0:
                j.speak("Opening Terminal...")

                class Thread5(Thread):
                    def run(self):
                        ter = subprocess.Popen("gnome-terminal")
                        stop.terminal(ter, 1)

                o5 = Thread5()
                o5.start()
                return 0
            elif "system setting" in usr_command:
                j.speak("opening setting")
                subprocess.Popen("/usr/bin/gnome-control-center")
                return 0

            elif usr_command.find("system monitor") >= 0:
                j.speak("Opening system-monitor...")

                class Thread2(Thread):
                    def run(self):
                        moni = subprocess.Popen("gnome-system-monitor")
                        stop.monitor(moni, 1)

                o2 = Thread2()
                o2.start()
                return 0
            elif "steam" in usr_command:
                print("Opening steam...")

                class Thread9(Thread):
                    def run(self):
                        steam = subprocess.Popen(
                            "/home/aman/.steam/steam.sh")
                        stop.steam(steam, 1)

                o9 = Thread9()
                o9.start()
                return 0
        ###################################                 COMMAND :   ELSE
        else:

            ##############                                  COMMUNICATION SKILL
            if "hello" in usr_command or "hii" in usr_command:
                j.speak("hello sir, how are you")
                return 0
            elif "fine" in usr_command:
                j.speak("I am happy to hear sir")
                return 0
            elif "nice" in usr_command:
                j.speak("thank you sir")
                return 0
            ###############################################
            elif "joke" in usr_command:
                urlj = "https://official-joke-api.appspot.com/random_ten"
                joke = requests.get(urlj).text
                joke_dect = json.loads(joke)
                # print(news_dect)
                joke_line = joke_dect
                for article in joke_line:
                    j.speak(article['setup'])
                    time.sleep(2)
                    j.speak(article['punchline'])
                    time.sleep(1)
                    playsound.playsound("/home/aman/PycharmProjects/JARVIS/data/shy_femail.mp3")
                    break
                return 0

            elif "volume" in usr_command:
                if "increase" in usr_command:
                    playlist.playlist(ipath=None, ival=None)
                else:
                    playlist.playlist(ipath=None, ival=None)
                return 0

            elif usr_command.find("switch") >= 0 and (usr_command.find("tab") >= 0 or "window" in usr_command):
                pyautogui.keyDown('alt')
                pyautogui.press('tab')
                time.sleep(0.5)
                pyautogui.keyUp('alt')
                return 0

            elif "read pdf" in usr_command:
                book = open(
                    '/home/aman/Documents/Assignment-210329-183610.pdf', 'rb')
                pdf_read = PyPDF2.PdfFileReader(book)
                pages = pdf_read.getNumPages()
                j.speak(f"PDF contain {pages} Number of pages")
                j.speak("Sir ,Please enter page number which I want to read")
                pg = int(input("Enter hear:"))
                page = pdf_read.getPage(pg)
                text = page.extractText()
                # j.speak(text)
                print(text.encode('utf-8'))
                return 0

            elif "send" in usr_command and ("send gmail" in usr_command or "send email" in usr_command
                                            or "send mail" in usr_command or usr_command.find("file") >= 0):
                sendMail.sendGmail(usr_command)
                return 0

            # elif "thread" in usr_command:
            #     # Thread1.is_alive()

            # kit.text_to_handwriting()
            # pywhatkit.shutdown(time=100)  # Will shutdown the system
            # pywhatkit.showHistory()
            # pywhatkit.cancelShutdown()  # Will cancel the scheduled shutdown
            # kit.playonyt()

            elif ("whatsapp" or "message") in usr_command:
                j.speak("sir ,To whom should i send")
                # print("Enter Contact Name:")
                contact_name = input("Enter Contact Name:")
                contact_name = contact_name.lower()
                contact_num = Wtsp.wtsp_num(contact_name)
                print("number:+", contact_num)

                class Thread21(Thread):
                    def run(self):
                        kit.sendwhatmsg(f"+{contact_num}", "Just ignore this message")
                        j.speak("Message sent")
                        time.sleep(5)
                        raise Exception

                object21 = Thread21()
                object21.start()

                return 0

            elif "alarm" in usr_command:
                Alarm.setAlarm(usr_command)
                j.speak("ok sir i will notify you")
                return 0

            elif "screenshot" in usr_command:
                global nameInt
                nameInt += 1
                shot = pyautogui.screenshot()
                shot.save(
                    "/home/aman/Pictures/ByJarvis{}.png".format(nameInt))
                j.speak("I saved It in 'Pictures'")
                return 0
            elif "system logout" in usr_command or "system lock" in usr_command:
                subprocess.Popen("/usr/bin/gnome-session-quit")
                j.speak("Are you ..sure...")
                return 0
            elif "todo" in usr_command:
                subprocess.Popen("/usr/bin/gnome-todo")
                j.speak("This is all about...TODO")
                return 0
            elif "properties" in usr_command:
                subprocess.Popen("/usr/bin/gnome-session-properties")
                j.speak("This is all about...Properties")
                return 0

            elif "time" in usr_command:
                j.speak(
                    "The time is " + str(datetime.datetime.now().strftime("%H hour and %M minutes")))
                return 0
            elif "date" in usr_command:
                j.speak("Today is " +
                        datetime.datetime.now().strftime("%d %B %Y"))
                return 0

            elif " day" in usr_command:
                j.speak("Today is " + datetime.datetime.now().strftime("%A"))
                return 0

            elif "weather" in usr_command:
                global humidity, humidity, arts
                j.speak("Mostly  " + arts)
                j.speak("Temperature " +
                        str(temperature - 273.15) + " degree Celsius")
                j.speak("Humidity " + str(humidity) + "%")
                return 0
            elif "again" in usr_command or "once more" in usr_command:
                global old_cmd
                print(old_cmd)
                brain(old_cmd)
                return 0

            elif "mute" in usr_command or "quite" in usr_command or "shutup" in usr_command or "sleep" in usr_command:
                j.speak("ok sir ,press key to wake me...")
                x = input()
                j.speak("Initiating system... \n i am ready, always for you sir")
                return 0
            elif "wikipedia" in usr_command:
                try:
                    usr_command = usr_command.replace("wikipedia", "")
                    result = wikipedia.summary(usr_command, sentences=1)
                    j.speak("According to wikipedia")
                    j.speak(result)
                except:
                    print("Sir Please check your internet connection!")
                return 0



            elif usr_command.find("quit jarvis") >= 0 or usr_command.find("good bye") >= 0 or usr_command.find(
                    "exit jarvis") >= 0 or usr_command.find("close jarvis") >= 0 or usr_command.find(
                "bye") >= 0 or usr_command.find("goodbye") >= 0:
                j.speak("Bye Sir,Hope you enjoyed!")
                sys.exit()

            elif usr_command.find("News") >= 0 or usr_command.find("headlines") >= 0:
                j.speak("Sir ,Please enter number of headlines you want to know.")
                line_num = int(input("Enter number of lines : "))
                News.news_of(line_num)
                return 0
            elif usr_command.find("toss") & usr_command.find("coin") >= 0:
                lst = ["HEADS", "TAILS"]
                j.speak(random.choice(lst))
                return 0
            elif usr_command.find("through") & usr_command.find("dice") >= 0:
                lst = [1, 2, 3, 4, 5, 6]
                j.speak(random.choice(lst))
                return 0
            elif usr_command.find("add") >= 0 or usr_command.find("+") >= 0:
                sp_list = usr_command.split(" ")
                num1 = 0.0
                for i in sp_list:
                    if i.isnumeric():
                        num1 = (num1 + float(i))
                j.speak(num1)
                return 0
            elif usr_command.find("subtract") >= 0 or usr_command.find("-") >= 0:
                sp_list = usr_command.split(" ")
                num1 = 0.0
                for i in sp_list:
                    if i.isnumeric():
                        num1 = (float(i) - num1)
                j.speak(num1)
                return 0
            elif usr_command.find("location") >= 0 or usr_command.find("where i am") >= 0:
                send_url = "http://api.ipstack.com/check?access_key=2e5cc084aed1721597ed30a2b5219112"
                geo_req = requests.get(send_url)
                geo_json = json.loads(geo_req.text)
                # latitude = geo_json['latitude']
                # longitude = geo_json['longitude']
                city = geo_json['city']
                state = geo_json['region_name']
                country = geo_json['country_name']
                # print(f"If i am not wrong, then you are in  .{city} {country} {geo_json}")
                j.speak(f"If i am not wrong, then you are in  .{city}. {state} .{country}")
                return 0

            elif usr_command.find("multiply") >= 0 or usr_command.find("*") >= 0:
                sp_list = usr_command.split(" ")
                num1 = 1.0
                for i in sp_list:
                    if i.isnumeric():
                        num1 = (num1 * float(i))
                j.speak(num1)
                return 0
            elif usr_command.find("divide") >= 0 or usr_command.find("/") >= 0:
                sp_list = usr_command.split(" ")
                num1 = []
                for i in sp_list:
                    if i.isnumeric():
                        num1.append(float(i))
                j.speak(num1[0] / num1[1])
                return 0
            else:
                j.speak("Sorry! sir ,Can you speak again")
                return 0
    # except TypeError as et:
    #     j.speak("Sorry! sir, an ERROR occupied, Try Something else.")
    #     print("ERROR " + str(et))
    #     return 0
    finally:
        store(usr_command)


startExecution = MainThread()


class Main(QMainWindow):
    global f

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        j.speak("Initiating.. System modules")
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startjarvis)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startjarvis(self):
        # main gif run
        self.ui.movie = QtGui.QMovie(
            "/home/aman/PycharmProjects/JARVIS/data/mainf.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        # initlization gif run
        self.ui.movie = QtGui.QMovie(
            "/home/aman/PycharmProjects/JARVIS/data/inslization.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()

        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start(1000)
        startExecution.start()

    def showtime(self):
        global f
        # datetime.datetime.now().strftime("%H hour and %M minutes")
        # textbox=background:transparent;\nfont: 75 11pt "Purisa";\ncolor:white;
        self.ui.textBrowser_2.setText(
            datetime.datetime.now().strftime("%H:%M"))  # :%S
        self.ui.textBrowser_3.setText(datetime.datetime.now().strftime("%A"))
        self.ui.textBrowser.setText(datetime.datetime.now().strftime("%B %Y"))
        self.ui.textBrowser_4.setText(datetime.datetime.now().strftime("%d"))
        self.ui.textBrowser_5.setText(datetime.datetime.now()
                                      .strftime(f"{arts}   |  {str(round(temperature - 273.15))}" +
                                                u"\N{DEGREE SIGN}C   | " + f" Humidity-{humidity}"))
        # self.ui.textBrowser_6.append(f.getvalue())


# global jarvis

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())
# class Thread56(Thread):
#     def run(self):
#
#         jarvis = Main()
#         jarvis.show()
#         exit(app.exec_())
#
#
# o57 = Thread56()
# o57.start()


# if __name__ == "__main__":
#     # wish_me()
#     terminate = 0
#     while terminate <= 0:
#         usrObj = speechRecog()
#         usr_command = usrObj.take_command()
#         terminate = brain()
#         continue
# thanks jarvis
# you can sleep
#