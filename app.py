from flask import Flask, redirect, url_for, render_template, request, session, flash,g, abort,send_from_directory, send_file,Response, make_response, current_app as app
from flask_session import Session 
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta,datetime,date
from vosk import Model, KaldiRecognizer, SetLogLevel
from lexical_diversity import lex_div as ld
import sys
import time 
import os
import wave
from fpdf import FPDF
import PyPDF2 
from datetime import datetime,date
from random import randint
import numpy as np
from scipy.io.wavfile import write
from random import randint
import sounddevice as sd 
import contextlib
import pandas as pd
import smtplib
import os
import soundfile
from fastpunct import FastPunct
from math import e
from scipy.io.wavfile import write
import wavio as wv
import myprosody as mysp
import pickle
import sys, io
from dotenv import load_dotenv
from fpdf import FPDF
import stripe
from grammarbot import GrammarBotClient
import collections

load_dotenv()
app = Flask(__name__)
SESSION_TYPE='filesystem'
app.config.from_object(__name__)
STRIPE_PUBLISHABLE_KEY = os.get_env("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY=  os.get_env("STRIPE_SECRET_KEY")
stripe.api_key=STRIPE_SECRET_KEY


Session(app)
app.permanent_session_lifetime = timedelta(minutes=30)  #How long you want to store session data? Put here

####HOME PAGE#######
@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
def home():
    session['mtld1']=0
    session['mtld2']=0
    session['mtld3']=0
    session['mtld']=0
    session['hdd1']=0
    session['hdd2']=0
    session['hdd3']=0
    session['hdd']=0
    session['ttr1']=0
    session['ttr2']=0
    session['ttr3']=0
    session['ttr']=0
    session['text1']=0
    session['text2']=0
    session['text3']=0
    session['speechrate1']=0
    session['speechrate2']=0
    session['speechrate3']=0
    session['speechrate']=0
    session['artrate1']=0
    session['artrate2']=0
    session['artrate3']=0
    session['artrate']=0
    session['pauses1']=0
    session['pauses2']=0
    session['pauses3']=0
    session['pauses']=0
    session['wpm1']=0
    session['wpm2']=0
    session['wpm3']=0
    session['wpm']=0
    #percentiles
    session['toefl1']=0
    session['toefl2']=0
    session['toefl3']=0
    session['toefl']=0
    session['intonation1']=0
    session['intonation2']=0
    session['intonation3']=0
    session['intonation']=0
    session['correct_vowels1']=0
    session['correct_vowels2']=0
    session['correct_vowels3']=0
    session['correct_vowels']=0
    session['vocd']=0
    session['ttr']=0
    session['hdd']=0
    session['mtld']=0
    session['wpm']=0
    session['speechrate']=0
    session['artrate']=0
    session['pauses']=0
    session['toefl']=0
    session['intonation']=0
    session['correct_vowels']=0
    session['text']=0
    questions=['What is the purpose of government?','How do you see your future?','Do you enjoy sports? Why? Why not? What sports?','If you could choose any activity to do in your free time, which activity would you choose & why?','What does your name mean to you?', 'What is/was your favorite subject in school? Tell me more.','What is your favorite food & why?','What is your favorite type of art and why?','What makes you annoyed? Why?']
    session['questions']=questions

    return render_template('index.html')

###Record1
@app.route('/record1', methods = ['GET', 'POST'])
def record1():
    m=randint(0,8)
    questions=session.get('questions')
    question1=questions[m]
    questions.pop(m)
    session['questions']=questions
    session['question1']=question1
    return render_template("record1.html",question1=question1)  

@app.route('/recording1', methods = ['GET', 'POST'])
def record_it_1():
    try:    
        if request.method == 'POST' or 'GET':
            ###making recording and running myprosody functions on it
            message=''
            question1=session['question1']
            # Sampling frequency
            freq = 48000
            # Recording duration
            duration = 60
            recording = sd.rec(int(duration * freq), 
                       samplerate=freq, channels=1,dtype='int32')
            # Record audio for the given number of seconds
            sd.wait()
            # Convert the NumPy array to audio file
            filename="recording1.wav"
            write(filename, freq, recording)
            
            stdout = sys.stdout
            sys.stdout = io.StringIO()
            p='recording1'
            c='myprosody'
            mysp.mysptotal(p,c)
            output = sys.stdout.getvalue()
            if output=='Try again the sound of the audio was not clear':
                message='Please Record Again.' 
            else:
                sys.stdout = stdout
            try:
                output1=output.split('rate_of_speech')
                speechrate1=output1[1].split('articulation_rate')
                speechrate1=speechrate1[0]
                speechrate1=speechrate1.replace(" ","")
                try:
                    speechrate1=float(speechrate1)
                except:
                    speechrate1='NA'
                output2=output.split('articulation_rate')
                artrate1=output2[1].split('speaking_duration')
                artrate1=artrate1[0]
                artrate1=artrate1.replace(" ","")
                try:
                    artrate1=float(artrate1)
                except:
                    artrate1="NA"
                output3=output.split('number_of_pauses')
                pauses1=output3[1].split('rate_of_speech')
                pauses1=pauses1[0]
                pauses1=pauses1.replace(" ","")
                try:
                    pauses1=float(pauses1)
                except:
                    pauses1='NA'
                stdout = sys.stdout
                sys.stdout = io.StringIO()
                mysp.myprosody(p,c)
                output = sys.stdout.getvalue()
                sys.stdout = stdout
                output1=output.split('TOEFL_Scale_Score:')
                toefl1=output1[1][0:10]
                try:
                    toefl1=float(toefl1)
                except:
                    toefl1='NA'
                output2=output.split('intonation_index:')
                intonation1=output2[1][0:10]
                try:
                    intonation1=float(intonation1)
                except:
                    intonation1='NA'
                output3=output.split('perc%._correct_vowel:')
                correct_vowels1=output3[1][0:10]
                try:
                    correct_vowels1=float(correct_vowels1)
                except:
                    correct_vowels1='NA'
                session['speechrate1']=speechrate1
                session['artrate1']=artrate1
                session['pauses1']=pauses1
                session['toefl1']=toefl1
                session['intonation1']=intonation1
                session['correct_vowels1']=correct_vowels1


                ###vosking the recorded file
                new_file='vosk_recording1.wav'
                data,samplerate=soundfile.read(filename)
                soundfile.write(new_file,data,samplerate,subtype='PCM_16')
                wf = wave.open(new_file, "rb")
                model = Model("model")
                rec = KaldiRecognizer(model, wf.getframerate())
                rec.SetWords(True)
                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if rec.AcceptWaveform(data):
                        pass
                    else:
                        pass

                text=rec.FinalResult()
                new_text=text.rsplit(']',1)
                new_text=new_text[-1]
                new_text=new_text[13:-2]  
                flt = ld.flemmatize(new_text)
                hdd1=ld.hdd(flt)
                mtld1=ld.mtld(flt)
                ttr1=ld.ttr(flt)
                text1=new_text
                wpm1=len(new_text.split(' '))
                session['hdd1']=hdd1
                session['mtld1']=mtld1
                session['ttr1']=ttr1
                session['text1']=text1
                session['wpm1']=wpm1
                session.modified=True
                message='Recorded Successfully!'
            except:
                message='Your recording might be too noisy. Please record again.'
            return render_template("record1.html",message=message,question1=question1) 
    except:
        return redirect(url_for('index.html'))
 
###Record2
@app.route('/record2', methods = ['GET', 'POST'])
def record2():
    m=randint(0,7)
    questions=session['questions']
    question2=questions[m]
    questions.pop(m)
    session['questions']=questions
    session['question2']=question2
    return render_template("record2.html",question2=question2)  

@app.route('/recording2', methods = ['GET', 'POST'])
def record_it_2():
    try:
        if request.method == 'POST' or 'GET':
            ###making recording and running myprosody functions on it
            message=''
            question2=session.get('question2')  
            # Sampling frequency
            freq = 48000
            # Recording duration
            duration = 60
            recording = sd.rec(int(duration * freq), 
                       samplerate=freq, channels=1,dtype='int32')
            # Record audio for the given number of seconds
            sd.wait()
            # Convert the NumPy array to audio file
            filename="recording2.wav"
            write(filename, freq, recording)
            
            stdout = sys.stdout
            sys.stdout = io.StringIO()
            p='recording2'
            c='myprosody'
            mysp.mysptotal(p,c)
            output = sys.stdout.getvalue()
            sys.stdout = stdout
            if output=='Try again the sound of the audio was not clear':
                message="Please Record again"
            else:
                sys.stdout = stdout
            try:
                output1=output.split('rate_of_speech')
                speechrate2=output1[1].split('articulation_rate')
                speechrate2=speechrate2[0]
                speechrate2=speechrate2.replace(" ","")
                try:
                    speechrate2=float(speechrate2)
                except:
                    speechrate2='NA'
                output2=output.split('articulation_rate')
                artrate2=output2[1].split('speaking_duration')
                artrate2=artrate2[0]
                artrate2=artrate2.replace(" ","")
                try:
                    artrate2=float(artrate2)
                except:
                    artrate2="NA"
                output3=output.split('number_of_pauses')
                pauses2=output3[1].split('rate_of_speech')
                pauses2=pauses2[0]
                pauses2=pauses2.replace(" ","")
                try:
                    pauses2=float(pauses2)
                except:
                    pauses2='NA'
                stdout = sys.stdout
                sys.stdout = io.StringIO()
                mysp.myprosody(p,c)
                output = sys.stdout.getvalue()
                sys.stdout = stdout
                output1=output.split('TOEFL_Scale_Score:')
                toefl2=output1[1][0:10]
                try:
                    toefl2=float(toefl2)
                except:
                    toefl2='NA'
                output2=output.split('intonation_index:')
                intonation2=output2[1][0:10]
                try:
                    intonation2=float(intonation2)
                except:
                    intonation2='NA'
                output3=output.split('perc%._correct_vowel:')
                correct_vowels2=output3[1][0:10]
                try:
                    correct_vowels2=float(correct_vowels2)
                except:
                    correct_vowels2='NA'
                session['speechrate2']=speechrate2
                session['artrate2']=artrate2
                session['pauses2']=pauses2
                session['toefl2']=toefl2
                session['intonation2']=intonation2
                session['correct_vowels2']=correct_vowels2


                ###vosking the recorded file
                new_file='vosk_recording2.wav'
                data,samplerate=soundfile.read(filename)
                soundfile.write(new_file,data,samplerate,subtype='PCM_16')
                wf = wave.open(new_file, "rb")
                model = Model("model")
                rec = KaldiRecognizer(model, wf.getframerate())
                rec.SetWords(True)
                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if rec.AcceptWaveform(data):
                        pass
                    else:
                        pass

                text=rec.FinalResult()
                new_text=text.rsplit(']',1)
                new_text=new_text[-1]
                new_text=new_text[13:-2]  
                flt = ld.flemmatize(new_text)
                hdd2=ld.hdd(flt)
                mtld2=ld.mtld(flt)
                ttr2=ld.ttr(flt)
                text2=new_text
                wpm2=len(new_text.split(' '))
                session['hdd2']=hdd2
                session['mtld2']=mtld2
                session['ttr2']=ttr2
                session['text2']=text2
                session['wpm2']=wpm2
                session.modified=True
                message='Recorded Successfully!'
            except:
                message='Your recording might be too noisy. Please record again.'
        return render_template("record2.html",message=message,question2=question2) 
    except:
        return redirect(url_for('index.html'))
###Record3
@app.route('/record3', methods = ['GET', 'POST'])
def record3():
    m=randint(0,6)
    questions=session.get('questions')
    question3=questions[m]
    questions.pop(m)
    session['questions']=questions
    session['question3']=question3
    return render_template("record3.html",question3=question3)  

@app.route('/recording3', methods = ['GET', 'POST'])
def record_it_3():
    try:
        if request.method == 'POST' or 'GET':
            ###making recording and running myprosody functions on it
            message=''
            question3=session.get('question3')
            # Sampling frequency
            freq = 48000
            # Recording duration
            duration = 60
            recording = sd.rec(int(duration * freq), 
                       samplerate=freq, channels=1,dtype='int32')
            # Record audio for the given number of seconds
            sd.wait()
            # Convert the NumPy array to audio file
            filename="recording3.wav"
            write(filename, freq, recording)
            
            stdout = sys.stdout
            sys.stdout = io.StringIO()
            p='recording3'
            c='myprosody'
            mysp.mysptotal(p,c)
            output = sys.stdout.getvalue()
            sys.stdout = stdout
            if output=='Try again the sound of the audio was not clear':
                message="Please Record again"
            else:
                sys.stdout = stdout
            try:
                output1=output.split('rate_of_speech')
                speechrate3=output1[1].split('articulation_rate')
                speechrate3=speechrate3[0]
                speechrate3=speechrate3.replace(" ","")
                try:
                    speechrate3=float(speechrate3)
                except:
                    speechrate3='NA'
                output2=output.split('articulation_rate')
                artrate3=output2[1].split('speaking_duration')
                artrate3=artrate3[0]
                artrate3=artrate3.replace(" ","")
                try:
                    artrate3=float(artrate3)
                except:
                    artrate3="NA"
                output3=output.split('number_of_pauses')
                pauses3=output3[1].split('rate_of_speech')
                pauses3=pauses3[0]
                pauses3=pauses3.replace(" ","")
                try:
                    pauses3=float(pauses3)
                except:
                    pauses3='NA'
                stdout = sys.stdout
                sys.stdout = io.StringIO()
                mysp.myprosody(p,c)
                output = sys.stdout.getvalue()
                sys.stdout = stdout
                output1=output.split('TOEFL_Scale_Score:')
                toefl3=output1[1][0:10]
                try:
                    toefl3=float(toefl3)
                except:
                    toefl3='NA'
                output2=output.split('intonation_index:')
                intonation3=output2[1][0:10]
                try:
                    intonation3=float(intonation3)
                except:
                    intonation3='NA'
                output3=output.split('perc%._correct_vowel:')
                correct_vowels3=output3[1][0:10]
                try:
                    correct_vowels3=float(correct_vowels3)
                except:
                    correct_vowels3='NA'
                session['speechrate3']=speechrate3
                session['artrate3']=artrate3
                session['pauses3']=pauses3
                session['toefl3']=toefl3
                session['intonation3']=intonation3
                session['correct_vowels3']=correct_vowels3


                ###vosking the recorded file
                new_file='vosk_recording3.wav'
                data,samplerate=soundfile.read(filename)
                soundfile.write(new_file,data,samplerate,subtype='PCM_16')
                wf = wave.open(new_file, "rb")
                model = Model("model")
                rec = KaldiRecognizer(model, wf.getframerate())
                rec.SetWords(True)
                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if rec.AcceptWaveform(data):
                        pass
                    else:
                        pass

                text=rec.FinalResult()
                new_text=text.rsplit(']',1)
                new_text=new_text[-1]
                new_text=new_text[13:-2]  
                flt = ld.flemmatize(new_text)
                hdd3=ld.hdd(flt)
                mtld3=ld.mtld(flt)
                ttr3=ld.ttr(flt)
                text3=new_text
                wpm3=len(new_text.split(' '))
                session['hdd3']=hdd3
                session['mtld3']=mtld3
                session['ttr3']=ttr3
                session['text3']=text3
                session['wpm3']=wpm3
                session.modified=True
                message='Recorded Successfully!'
            except:
                message='Your recording might be too noisy. Please record again.'
        return render_template("record3.html",message=message,question3=question3) 
    except:
        return redirect(url_for('index.html'))

####Results#####
@app.route("/results",methods=['GET','POST'])
def results():
    if session.get('mtld1') or session.get('mtld2') or session.get('mtld3') is not None:
        mtld=round(((session.get('mtld1')+session.get('mtld2')+session.get('mtld3'))/3),2)
        hdd=round(((session.get('hdd1')+session.get('hdd2')+session.get('hdd3'))/3),2)
        ttr=round(((session.get('ttr1')+session.get('ttr2')+session.get('ttr3'))/3),2)
        vocd=round((75.08*(e**(.14*hdd))),2)
        if hdd==0:
            vocd=0
        if vocd>=80:
            interp='Your spoken samples indicate your lexical diversity is equivalent to an adult<br> native language speaker who is writing academic text. Typically, this ranges between a VOC-D score of 80-105.'
        elif 71<=vocd<=79:
            interp='Your spoken samples indicate your lexical diversity is equivalent to an adult<br> advanced ESL scholar or more casual speech of a native speaker.'
        elif 40<=vocd<=70:
            interp='Your spoken samples indicate your lexical diversity is equivalent to an adult ESL student. Typically, this ranges between a VOC-D score of 40-70.'
        else:
            interp='Your spoken samples indicate your lexical diversity is below that of an average adult native speaker.<br>Please see the "FAQS" page for more info on other English speaking populations that may have lower VOC-D scores.'
        text1=session.get('text1')
        text2=session.get('text2')
        text3=session.get('text3')
        text1=f'Recording1: {text1}'
        text2=f'Recording2: {text2}'
        text3=f'Recording3: {text3}'
        speechrate1=session['speechrate1']
        speechrate2=session['speechrate2']
        speechrate3=session['speechrate3']
        speechrate=round(((speechrate1+speechrate2+speechrate3)/3),2)
        artrate1=session['artrate1']
        artrate2=session['artrate2']
        artrate3=session['artrate3']
        artrate=round(((artrate1+artrate2+artrate3)/3),2)
        pauses1=session['pauses1']
        pauses2=session['pauses2']
        pauses3=session['pauses3']
        pauses=round(((pauses1+pauses2+pauses3)/3),2)
        wpm1=session['wpm1']
        wpm2=session['wpm2']
        wpm3=session['wpm3']
        try:
            wpm=round(((wpm1+wpm2+wpm3)/3),2)
        except:
            wpm='NA'
        
        #percentiles
        toefl1=session['toefl1']
        toefl2=session['toefl2']
        toefl3=session['toefl3']
        try:
            toefl=round(((toefl1+toefl2+toefl3)/3),2)
        except:
            toefl='NA' 
        intonation1=session['intonation1']
        intonation2=session['intonation2']
        intonation3=session['intonation3']
        try:
            intonation=round(((intonation1+intonation2+intonation3)/3),2)
        except:
            intonation='NA'
        correct_vowels1=session['correct_vowels1']
        correct_vowels2=session['correct_vowels2']
        correct_vowels3=session['correct_vowels3']
        try:
            correct_vowels=round(((correct_vowels1+correct_vowels2+correct_vowels3)/3),2)
        except:
            correct_vowels='NA'
        
        results=f'VOC-D: {vocd},<br>TTR: {ttr},<br>HD-D: {hdd},<br>MTLD: {mtld}<br>WPM: {wpm} words/minute<br>Speaking Rate: {speechrate} syll/s<br>Articulation Rate: {artrate} syll/s'
        session.pop('mtld1',None)
        session.pop('mtld2',None)
        session.pop('mtld3',None)  
        session.pop('hdd1',None)
        session.pop('hdd2',None)
        session.pop('hdd3',None) 
        session.pop('ttr1',None)
        session.pop('ttr2',None)
        session.pop('ttr3',None) 
        session.pop('text1',None)
        session.pop('text2',None)
        session.pop('text3',None) 
        session.pop('speechrate1',None)
        session.pop('speechrate2',None)
        session.pop('speechrate3',None)
        session.pop('artrate1',None)
        session.pop('artrate2',None)
        session.pop('artrate3',None)
        session.pop('pauses1',None)
        session.pop('pauses2',None)
        session.pop('pauses3',None)
        session.pop('wpm1',None)
        session.pop('wpm2',None)
        session.pop('wpm3',None)
        #percentiles
        session.pop('toefl1',None)
        session.pop('toefl2',None)
        session.pop('toefl3',None)
        session.pop('intonation1',None)
        session.pop('intonation2',None)
        session.pop('intonation3',None)
        session.pop('correct_vowels1',None)
        session.pop('correct_vowels2',None)
        session.pop('correct_vowels3',None)
        session.pop('questions',None)
        if os.path.exists("recording1.wav"):
            os.remove("recording1.wav")
        if os.path.exists("recording2.wav"):
            os.remove("recording2.wav")
        if os.path.exists("recording3.wav"):
            os.remove("recording3.wav")
        if os.path.exists("recording1.TextGrid"):
            os.remove("recording1.TextGrid")
        if os.path.exists("recording2.TextGrid"):
            os.remove("recording2.TextGrid")
        if os.path.exists("recording3.TextGrid"):
            os.remove("recording3.TextGrid")
        if os.path.exists('vosk_recording1.wav'):
            os.remove('vosk_recording1.wav')
        if os.path.exists('vosk_recording2.wav'):
            os.remove('vosk_recording2.wav')
        if os.path.exists('vosk_recording3.wav'):
            os.remove('vosk_recording3.wav')
    else:
        mtld='NA'
        ttr='NA'
        hdd='NA'
        vocd='NA'
        results='NA'
        interp='NA'
        text1='NA'
        text2='NA'
        text3='NA'
        wpm='NA'
        speechrate='NA'
        artrate='NA'
        pauses='NA'
        toefl='NA'
        intonation='NA'
        correct_vowels='NA'

    text=[text1,text2,text3]
    session['vocd']=vocd
    session['ttr']=ttr
    session['hdd']=hdd
    session['mtld']=mtld
    session['wpm']=wpm
    session['speechrate']=speechrate
    session['artrate']=artrate
    session['pauses']=pauses
    session['toefl']=toefl
    session['intonation']=intonation
    session['correct_vowels']=correct_vowels
    session['text']=text
    results=f'VOC-D: {vocd},<br>TTR: {ttr},<br>HD-D: {hdd},<br>MTLD: {mtld}<br>WPM: {wpm} words/minute<br>Speaking Rate: {speechrate} syll/s<br>Articulation Rate: {artrate} syll/s'
    return render_template('results.html',results=results,interp=interp)

@app.route('/stripe_pay',methods=['POST'])
def stripe_pay():

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price':'price_1JIJinLRlFxJI9dpO3gjN2ov',
            'quantity':1,},],
        mode='payment',
        allow_promotion_codes=True,
        success_url=url_for('report', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('home', _external=True),
    )
    return redirect(session.url,code=303)


####Report####
@app.route('/report')
def report():
    password=randint(11111,99999)
    session['password']=password
    return render_template('report.html',password=password)

@app.route('/get_report', methods=['POST','GET']) # this is a job for GET, not POST
def get_report():
    fullname=request.form['fullname']
    text=session.get('text')
    text1=text[0]
    text2=text[1]
    text3=text[2]
    vocd=session.get('vocd')
    ttr=session.get('ttr')
    hdd=session.get('hdd')
    mtld=session.get('mtld')
    wpm=session.get('wpm')
    speechrate=session.get('speechrate')
    artrate=session.get('artrate')
    pauses=session.get('pauses')
    toefl=session.get('toefl')
    intonation=session.get('intonation')
    correct_vowels=session.get('correct_vowels')
    try:
        diff=float(speechrate)-float(artrate)
    except:
        diff='NA'
    client = GrammarBotClient()
    if text1!='NA' and text1!=0:
        fastpunct = FastPunct()
        y=fastpunct.punct([text1],correct=True)
        text1_split=''
        text1_split=text1_split.join(y)
        ###TEXTONE#####
        text = text1
        res = client.check(text) #inspect text and stores it to a list
        y=res.matches #returns list of errors
        new_list=[]
        rules=[]
        for x in y:
            if x.category=='GRAMMAR':
                new_list.append(x)
            else:
                pass
        for x in new_list:
            rules.append(x.rule)
            

        error_occurrences = collections.Counter(rules)
        values=error_occurrences.values()
        total_errors=sum(values)

        error_text=''
        for item in error_occurrences:
            error_text+= str(item) +': '+str(error_occurrences[item])+ '\n'
        tot_words=len(text)
        rate=(total_errors/tot_words)
        if rate>.05:
            gram_qual=round(((1-(rate)+.05)*100),2)
        else:
            gram_qual=100
        ###IMPORTANT VARIABLES TO PASS TO CLIENT
        error_text1=error_text
        total_errors1=total_errors
        gram_qual1=gram_qual
    if text2!='NA' and text2!=0:
        y=fastpunct.punct([text2],correct=True)
        text2_split=''
        text2_split=text2_split.join(y)
        ####TEXTTWO#####
        text = text2
        res = client.check(text) #inspect text and stores it to a list
        y=res.matches #returns list of errors
        new_list=[]
        rules=[]
        for x in y:
            if x.category=='GRAMMAR':
                new_list.append(x)
            else:
                pass
        for x in new_list:
            rules.append(x.rule)
            

        error_occurrences = collections.Counter(rules)
        values=error_occurrences.values()
        total_errors=sum(values)

        error_text=''
        for item in error_occurrences:
            error_text+= str(item) +': '+str(error_occurrences[item])+ '\n'
        tot_words=len(text)
        rate=(total_errors/tot_words)
        if rate>.05:
            gram_qual=round(((1-(rate)+.05)*100),2)
        else:
            gram_qual=100
        
        ###IMPORTANT VARIABLES TO PASS TO CLIENT
        error_text2=error_text
        total_errors2=total_errors
        gram_qual2=gram_qual
    if text3!='NA' and text3!=0:
        y=fastpunct.punct([text3],correct=True)
        text3_split=''
        text3_split=text3_split.join(y)
        ###TEXTTHREE#####
        text = text3
        res = client.check(text) #inspect text and stores it to a list
        y=res.matches #returns list of errors
        new_list=[]
        rules=[]
        for x in y:
            if x.category=='GRAMMAR':
                new_list.append(x)
            else:
                pass
        for x in new_list:
            rules.append(x.rule)
            

        error_occurrences = collections.Counter(rules)
        values=error_occurrences.values()
        total_errors=sum(values)

        error_text=''
        for item in error_occurrences:
            error_text+= str(item) +': '+str(error_occurrences[item])+ '\n'
        tot_words=len(text)
        rate=(total_errors/tot_words)
        if rate>.05:
            gram_qual=round(((1-(rate)+.05)*100),2)
        else:
            gram_qual=100
        
        ###IMPORTANT VARIABLES TO PASS TO CLIENT
        error_text3=error_text
        total_errors3=total_errors
        gram_qual3=gram_qual
    if text1!='NA' and text1!=0 and text2!='NA' and text2!=0 and text3!='NA' and text3!=0:
        total_total_errors=total_errors1+total_errors2+total_errors3
        total_gram_qual=round(((gram_qual1+gram_qual2+gram_qual3)/3),2)
        total_gram_qual=str(total_gram_qual)+'%'
    else:
        total_total_errors='NA'
        total_gram_qual='NA'
        error_text1='NA'
        error_text2='NA'
        error_text3='NA'
        text1_split='NA'
        text2_split='NA'
        text3_split='NA'

    title='FluencyPredictor: Results & Analysis'
    ld_results=f'VOCD: {vocd}; TTR: {ttr}; HD-D: {hdd}; MTLD: {mtld};'
    ld_interp='This is what your Lexical Diversity scores mean...'
    prosody_results=f'Words-per-Minute: {wpm}; Speech Rate: {speechrate} syll/s; Articulation Rate: {artrate} syll/s; Intonation Index: {intonation};'
    prosody_interp='This is what your prosody scores mean...'
    grammar_results=f'Errors from Recording1: {error_text1}; Errors from Recording2: {error_text2};Errors from Recording3: {error_text3}; Total Errors: {total_total_errors}; Grammatic Quality Score: {total_gram_qual}'
    grammar_interp='This is where your grammar score is interpretted...'
    artic_results=f'Difference between Speech Rate and Articulation Rate: {diff}; Percentage of Correct Vowels: {correct_vowels}; Formant Centralization Ratio: 0'
    artic_interp='This is where your articulation interpretation is given...'
    fluency_results=f'TOEFL Score Estimate: {toefl}; Average Number of Pauses: {pauses};'
    fluency_interp='This is where your fluency is interpretted...'
    ref='These are references for scientific papers!'
    '''
    TOEFL speaking scale score
    Advanced (25–30)
    High-Intermediate (20–24)
    Low-Intermediate (16–19)
    Basic (10–15)
    Below Basic (0–9)
    '''
    question1=session.get('question1')
    question2=session.get('question2')
    question3=session.get('question3')
    password=session.get('password')
    title='Report of Results and Analysis'
    class PDF(FPDF):
        def header(self):
            # Arial bold 15
            # Calculate width of title and position
            #w = self.get_string_width(title) + 6
            self.set_x(10)
            # Colors of frame, background and text
            self.set_draw_color(0, 0, 0)
            self.set_fill_color(0,0,0)
            self.set_text_color(255, 255, 255)
            # Thickness of frame (1 mm)
            self.set_line_width(.25)
            # Title
            name='/logo_pdf.png'
            self.image(name, x = None, y = None, w = 190,type = 'PNG')
            self.ln()
        def body(self, txt):
            # Read text file
            # Times 12
            self.set_font('Times', '', 12)
            # Output justified text
            self.multi_cell(0, 5, txt)
            # Line break
            self.ln()

        # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.ln(4)
    pdf.set_font('Times', 'U', 18)
    pdf.cell(0,10, title,0,1,'C')
    pdf.set_font('Times', '', 11)
    pdf.cell(0, 10, f'Name: {fullname}', 0, 1,'L')
    pdf.cell(10, 10, f'Date and Time: {datetime.now()}', 0, 1,'L')
    pdf.ln(2)
    pdf.set_font('Times', '', 16)
    pdf.cell(100, 10, 'Transcripts:', 0, 1,'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(100, 10, f'{question1}', 0, 1,'L')
    pdf.body(text1_split)
    pdf.cell(100, 10, f'{question2}', 0, 1,'L')
    pdf.body(text2_split)
    pdf.cell(100, 10, f'{question3}', 0, 1,'L')
    pdf.body(text3_split)

    pdf.set_font('Times', '', 16)
    pdf.cell(250, 10, 'Grammar:', 0, 1,'L')
    pdf.set_font('Times', '', 12)
    pdf.body(grammar_results)
    pdf.body(grammar_interp)

    pdf.set_font('Times', '', 16)
    pdf.cell(250, 10, 'Articulation:', 0, 1,'L')
    pdf.set_font('Times', '', 12)
    pdf.body(artic_results)
    pdf.body(artic_interp)
    
    pdf.set_font('Times', '', 16)
    pdf.cell(200, 10, 'Prosody:', 0, 1,'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(150, 10, prosody_results, 0, 1,'L')
    pdf.body(prosody_interp)
    
    pdf.set_font('Times', '', 16)
    pdf.cell(150, 10, 'Lexical Diversity:', 0, 1,'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(150, 10, ld_results, 0, 1,'L')
    pdf.body(ld_interp)
    
    
    pdf.set_font('Times', '', 16)
    pdf.cell(200, 10, 'Fluency:', 0, 1,'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(150, 10, fluency_results, 0, 1,'L')
    pdf.body(fluency_interp)

    pdf.set_font('Times', '', 16)
    pdf.cell(200, 10, 'Unhappy with your results?', 0, 1,'L')
    pdf.set_font('Times', '', 12)
    pdf.body("We know this entire process isn't a complete science. Enter the promo code below during check out for two more tries that are 90% off. Promo code only lasts the duration of one month. Promo Code: TRYAGAIN")

    pdf.set_font('Times', '', 16)
    pdf.cell(250, 10, 'References:', 0, 1,'L')
    pdf.set_font('Times', '', 12)
    pdf.body(ref)
    filename_=f'FluencyPredictor_Report_{fullname}.pdf'
    pdf.output(name=filename_,dest='F')
    
    pdf_writer=PyPDF2.PdfFileWriter()
    pdf_reader=PyPDF2.PdfFileReader(filename_)
    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))
    pdf_writer.encrypt(user_pwd=str(password),owner_pwd=None,use_128bit=True)
    with open(filename_,'wb') as f:
        pdf_writer.write(f)
    return send_file(f'{filename_}', attachment_filename=filename_)     

@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'YOUR_ENDPOINT_SECRET'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}

####AboutUs#####
@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')

####FAQS#####
@app.route("/faqs")
def faqs():
    return render_template('faqs.html')

####CONTACT US####

@app.route("/contactus", methods=['GET','POST'])
def contactus():
    return render_template('contactus.html')
@app.route("/form",methods=["POST"])
def form():
    email=request.form["email"]
    message=request.form["message"]
    text="FluencyPredictor<br>Someone sent you a message<br>Email: "+email+"<br>Message:<br>"+message
    if not email or not message:
        info_text="Please enter all the correct information."
        return render_template("contactus.html",info_text=info_text)
    else:
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("",f'{os.getenv("PASSWORD")}')
        server.sendmail("","",text)
        info_text="Message sent!"
        return render_template("contactus.html",info_text=info_text)

if __name__ == "__main__":
	app.run(debug=True,port=4242)