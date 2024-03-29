#import for twitter
import tweepy
#import for sms services
from twilio.rest import Client
#import for U.I
from tkinter import Entry, Label, Button
import tkinter
#imports for IBM watson
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

#twitter junk
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
#twilio connection
client = Client("", "")

#ibm watson authentification
authenticator = IAMAuthenticator('')
service = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    authenticator=authenticator)
#connects to the language api
service.set_service_url('https://gateway.watsonplatform.net/natural-language-understanding/api')


def proces():
    #creates and opens gui to input phone numbers
    file = open("PhoneNumbers.txt", "a+")
    number1=Entry.get(E1)

    file.write(str(number1)+ '\n')
    file.close()

top = tkinter.Tk()
top.title("Twitter Notification System")
L1 = Label(top, text="Recieve alerts now!",font=("Arial Bold",10)).grid(row=0,column=1)
L2 = Label(top, text="Phone Number",font=("Arial Bold",8)).grid(row=2,column=0)
L2 = Label(top, text="",).grid(row=3,column=0)
L2 = Label(top, text="",).grid(row=3,column=0)
L2 = Label(top, text="",).grid(row=4,column=0)
L2 = Label(top, text="",).grid(row=5,column=0)
L2 = Label(top, text="",).grid(row=6,column=0)
top.geometry('350x150')
E1 = Entry(top, bd =5)
E1.grid(row=2,column=1)
B=Button(top, text ="Submit",command = proces).grid(row=4,column=1,)
C=Button(top, text ="close",command = top.destroy).grid(row=5,column=1)
 
top.mainloop()

class MyStreamListener(tweepy.StreamListener):

 def on_status(self, tweet):
     #checks if tweet is not a retweet
     if (not tweet.retweeted) and ('RT @' not in tweet.text):
        file=open("tweet_data.txt", "w+")
       
        #msg being saved to tweet data file
        pl = (tweet.text + "\n")
        #text message being sent
        print(pl)
        data = ("Alert!" + "\n" + tweet.user.screen_name + " has just sent a notification on twitter regarding a wildfire that has been deemed legitimate " + "\nLocation: " + tweet.user.location + "\nContent: " + tweet.text)
        file.write(pl)
        file.close()
        
        #opens tweet text file
        file=open("tweet_data.txt", "r")
        if file.mode == 'r':
            reader =file.readlines()
            #put data into watson
            for x in reader:
                response = service.analyze(
                        text=x,
                        features=Features(entities=EntitiesOptions(),
                                          keywords=KeywordsOptions())).get_result()
                if response["keywords"][0]["relevance"] > .4:
                    file_phones=open("PhoneNumbers.txt", "r")
                    #checks if file is in read mode
                    if file_phones.mode == 'r':
                        #reads each line from file
                        fl =file_phones.readlines()
                        for x in fl:
                            #texts user 
                            client.messages.create(to="+1" + x,
                                                       from_="", 
                                                       body=data)            
                    file_phones.close()
        #close file
        file.close()

#handles twitter feed listener
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['#test'])