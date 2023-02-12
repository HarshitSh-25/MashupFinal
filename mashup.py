from flask import Flask, render_template,request
import pandas as pd
import numpy as np
import sys
import os
import youtube_dl # client to download from many multimedia portals
import glob # directory operations
import os # interface to os-provided info on files
import sys # interface to command line
from pydub import AudioSegment # only audio operations
from pytube import YouTube
import zipfile
from youtubesearchpython import VideosSearch
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def download_audio(yt_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])

app=Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html')

@app.route('/',methods=['POST'])
def getvalue():
    name=request.form['name']
    number=request.form['number']
    duration=request.form['duration']
    email=request.form['email']
    # print(name+"---"+email)
    main(name, number, duration, email)
    return "<h1><center>Thanks</center></h1>"


@app.route('/login')
def login():
    return "<h1>Welcome</h1>"


def main(arg1,arg2,arg3,arg4):


    name=arg1
    videos=int(arg2)
    duration=arg3
    email=arg4
    output="final.mp3"
    # name="diljit dosanjh
    # videos=3
    # duration=3
    # output="lol"
    # name=sys.argv[1]
    # videos=int(sys.argv[2])
    # duration=sys.argv[3]
    # output=sys.argv[4]
    # print(name)
    # print(videos)
    # print(duration)
    # print(output)
    # print(sys.argv[0])

    videosSearch = VideosSearch(name, limit = videos)
    links=[]
    for i in range(0,videos):
        links.append(videosSearch.result()["result"][i]["link"])


    for i in range(0,videos):
        yt_url = links[i]
        download_audio(yt_url)
        initial = "00:00"
        final = "00:"
        if(int(duration) < 10):
            final+="0"
        final+=duration
        filename = newest_mp3_filename()
        trimmed_file = get_trimmed(filename, initial, final)
        os.remove(filename)
        newfile="audio"+str(i)+".mp3"
        trimmed_file.export(newfile, format="mp3")
    audio0 = AudioSegment.from_mp3("audio0.mp3")
    temp=AudioSegment.from_mp3("audio0.mp3")
    for i in range(1,videos):
        file="audio"+str(i)+".mp3"
        audio=AudioSegment.from_mp3(file)
        os.remove(file)
        audio0=audio0.append(audio)
    audio0.export(output,format="mp3")
    os.remove("audio0.mp3")
    zip = zipfile.ZipFile("final_z"+".zip", "w", zipfile.ZIP_DEFLATED)
    zip.write(output)
    zip.close()

    fromaddr = "Enter your email id"
    toaddr = email
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "102003653_HarshitSharma_Mashup"
    filename = "final_z.zip"
    attachment = open("final_z.zip", "rb")
    p = MIMEBase('application',  'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "Enter the password of your email id")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


def newest_mp3_filename():
    list_of_mp3s = glob.glob('./*.mp3')
    return max(list_of_mp3s, key = os.path.getctime)

def get_video_time_in_ms(video_timestamp):
    vt_split = video_timestamp.split(":")
    if (len(vt_split) == 3):
        hours = int(vt_split[0]) * 60 * 60 * 1000
        minutes = int(vt_split[1]) * 60 * 1000
        seconds = int(vt_split[2]) * 1000
    else:
        hours = 0
        minutes = int(vt_split[0]) * 60 * 1000
        seconds = int(vt_split[1]) * 1000
    # time point in miliseconds
    return hours + minutes + seconds

def get_trimmed(mp3_filename, initial, final = ""):
    if (not mp3_filename):
        # raise an error to immediately halt program execution
        raise Exception("No MP3 found in local directory.")
    # reads mp3 as a PyDub object
    sound = AudioSegment.from_mp3(mp3_filename)
    t0 = get_video_time_in_ms(initial)
    print("Beginning trimming process for file ", mp3_filename, ".\n")
    print("Starting from ", initial, "...")
    if (len(final) > 0):
        print("...up to ", final, ".\n")
        t1 = get_video_time_in_ms(final)
        return sound[t0:t1] # t0 up to t1
    return sound[t0:] # t0 up to the end



# downloads yt_url to the same directory from which the script runs
def download_audio(yt_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])


if __name__=='__main__':
    app.run(debug=True)