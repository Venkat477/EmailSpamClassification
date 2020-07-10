# EmailSpamClassification

This is a service, which takes an email as an input and check whether the Email is **SPAM or Not SPAM**. Below were the required input fields to test the app.

***1. From Address </br>
2. Email Subject </br>
3. Original HTML (We can get it from Email Options--> Show Original (In GMail)***

This a basic project on classifying an Email as SPAM or Not SPAM, for that I have used a Python package called **spamcheck**(https://pypi.org/project/spamcheck/) which is a simple python wrapper for Postmark's Spamcheck API

Based on the user input, will try to structure the email based on the email standards and will pass the email to wrapper which will tell us an email is SPAM or Not SPAM

I normalized the score between 0 to 5. **Anything less than 2.5 considered as SPAM and above as Not SPAM.**

***1. I have used Regex Patterns for removing all the unwanted characters and for identifying some key phrases. </br>
2. I have used Pandas for SPAM reasons processing </br>
3. I have used Plotly to display SPAM Score graph.***

**Programming Language:** Python3.7

Test the webapp using the given link (https://email-spamclassification.herokuapp.com/)
