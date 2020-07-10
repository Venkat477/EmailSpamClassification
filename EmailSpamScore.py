# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 02:20:31 2020
@author: Venkata N Divi
"""

import pandas as pd
import sys,streamlit as st
import plotly.graph_objects as go
from spamService import spamClassification

def processSPAM():
    try:
        st.subheader("**Try our Email SPAM Classification**")
        fromAddress_ = st.text_input("From Address")
        subject_ = st.text_input("Subject",key='subject')
        email_ = st.text_area("Email Content")
        
        if st.button('Classify'):
            spamSer = spamClassification()
            if len(subject_)>1 and len(fromAddress_)>1 and len(email_)>1:
                st.success('Analyzing Your Email, Please wait!!!')
                try:
                    html_ = email_.encode("ascii","ignore").decode('utf-8')
                    html_ = spamSer.getHTMLContent(html_).replace('= ','')
                    final_result = spamSer.spamV2finalService(subject_,fromAddress_,html_)
                    mainTitle = 'SPAM Score: '+"{:.2f}".format(final_result['spam_result']['score'])+'    Email Classification: '+final_result['spam_result']['class']
                    st.title('SPAM Score')
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = float("{:.2f}".format(final_result['spam_result']['score'])),
                        gauge = {'axis': {'range': [0, 5]},
                                 'bar': {'color': "orange"},
                         'steps' : [
                             {'range': [0, 1], 'color': "darkgreen"},
                             {'range': [1, 2], 'color': "darkolivegreen"},
                             {'range': [2, 3], 'color': "mediumseagreen"},
                             {'range': [3, 4], 'color': "red"},
                             {'range': [4, 5], 'color': "darkred"}],
                         'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75,'value': 2.5}},
                        
                        title = {'text': mainTitle, 'font': {'size': 24}}))
                    
                    st.plotly_chart(fig, use_container_width=True)
                    spamRes = final_result['spam_result']['reasons']
                    st.title('SPAM Score Report')
                    st.subheader('SPAM Score: **'+"{:.2f}".format(final_result['spam_result']['score'])+'**')
                    st.subheader('Your Email is classified as **'+final_result['spam_result']['class']+'**')
                    st.subheader('**SPAM Reasons**')
                    st.write(pd.DataFrame(spamRes))
                        
                except Exception as e:
                    print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),Exception, e)
            else:
                st.warning('Please try to enter all the fields!!!')
    except Exception as e:
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),Exception, e)

def selectOptions():
    try:
        st.write("This is a service, which takes an email as an input and check whether the Email is SPAM or Not SPAM. Below were the required input fields to test the app.")
        st.write("""
        - **From Address**
        - **Email Subject**
        - **Original HTML (We can get it from Email Options--> Show Original (In GMail)**""")
        
        st.write("""This a basic project on classifying an Email as SPAM or Not SPAM, for that I have used
        a Python package called **spamcheck** which is a simple python wrapper for Postmark's Spamcheck API""")
        st.write("""Based on the user input, will try to structure the email and will pass the email to
        wrapper which will tell us an email is SPAM or Not SPAM""")
        st.write("""I normalized the score between 0 to 5. Anything less than 2.5 considered as SPAM and above as Not SPAM""")
        st.write("""I have used Regex Patterns for removing all the unwanted characters and for identifying 
        some key phrases.""")
        st.write("""I have used Pandas for SPAM reasons processing and Plotly to display graphs.""")
        st.subheader('**Use the Left Side Options to test the Service**')
    except Exception as e:
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),Exception, e)

def main():
    try:
        st.sidebar.title("Email SPAM Classification")
        st.sidebar.markdown("Is your Email is SPAM Free? 📧")
        st.sidebar.subheader("Choose")
        activities=["Select","Email SPAM Classification"]
        choice = st.sidebar.selectbox("",activities)
        
        if choice == 'Select':
            selectOptions()
        elif choice == 'Email SPAM Classification':
            processSPAM()
    except Exception as e:
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),Exception, e)

if __name__ == '__main__':
    st.write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="X-UA-Compatible" content="ie=edge"><title>Responsive Navigation Bar - W3jar.Com</title><style>*,*::before,*::after {  box-sizing: border-box;  -webkit-box-sizing: border-box;}body {  font-family: sans-serif;  margin: 0;  padding: 0;}.container {  height: 80px;  background-color: #052252;  display: -webkit-box;  display: -ms-flexbox;  display: flex;  -ms-flex-wrap: wrap;  flex-wrap: wrap;  -webkit-box-align: center;  -ms-flex-align: center;  align-items: center;  overflow: hidden;}.container .logo {  max-width: 250px;  padding: 0 10px;  overflow: hidden;}.container .logo a {  display: -webkit-box;  display: -ms-flexbox;  display: flex;  -ms-flex-wrap: wrap;  flex-wrap: wrap;  -webkit-box-align: center;  -ms-flex-align: center;  align-items: center;  height: 60px;}.container .logo a img {  max-width: 100%;  max-height: 60px;}@media only screen and (max-width: 650px) {  .container {    -webkit-box-pack: justify;    -ms-flex-pack: justify;    justify-content: space-between;  }  .container .logo {    -webkit-box-flex: 1;    -ms-flex: 1;    flex: 1;  }}.body {  max-width: 700px;  margin: 0 auto;  padding: 10px;}</style></head><body><div class="container">    <div class="logo">    <a href="#"><img src="https://www.pngfind.com/pngs/m/663-6637558_png-file-svg-mail-spam-icon-png-transparent.png" alt="logo"></a>    </div></body></html>', unsafe_allow_html=True)
    st.title("Email SPAM Classification")
    st.markdown("Is your Email is SPAM Free? 📧")
    main()