# GUI for T2S converter 
import tkinter as tk #help to create GUI interface 
import boto3 #boto3 is python sdk for aws
import os #as we maybe require some temporary directory or some paths
import sys #to get current working dir and paths
from tempfile import gettempdir #we'll be storing the converted speech to some temporary dir
from contextlib import closing #to extract audio as a stream and close that file
root=tk.Tk()
root.geometry("400x240") #size of window
root.title("T2S-Con Amazon Polly") #root is handler for window
textExample=tk.Text(root,height=10) #to add a text area in my window
textExample.pack()
def getText():
    aws_mag_con=boto3.session.Session(profile_name='demo_user') #to login aws console by creating a session for it
    client=aws_mag_con.client(service_name='polly',region_name='us-east-1') #to call polly from aws mag console
    # IAM AND S3 ARE GLOBAL SERVICE SO NO NEED OF SPECIFYING REGION NAME.. BUT FOR OTHERS WE HAVE TO SPECIFY REGION NAME
    result=textExample.get("1.0","end") #1.0 means input is read from 1st point till the end
    print(result)
    response=client.synthesize_speech(VoiceId='Joanna',OutputFormat='mp3',Text=result, Engine='neural')
    print(response)
    if "AudioStream" in response:
        with closing(response['AudioStream']) as stream:
            output=os.path.join(gettempdir(),"speech.mp3") #extracted audio stream from response and in output I gave complete path of temp dir where this speech is stored along with its name
            try:
               with open(output,"wb") as file: #wb= with binary
                   file.write(stream.read()) # writing output as binary stream
            except IOError as error:
                print(error)
                sys.exit(-1) #exit gracefully if file not able to open
    else:
        print("Could not find the stream!") #if there is no audio stream
        sys.exit(-1)
    if sys.platform=='win32': #if we have windows
        os.startfile(output) #opens up media player i.e. opens file from temp dir
btnRead=tk.Button(root,height=1,width=10,text="Read",command=getText)
btnRead.pack()

root.mainloop() #will keep my window open until I cross it