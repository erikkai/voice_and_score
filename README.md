# voice_and_score
Block robocalls and other fraudulent callers by combining TeleSign's Score and Voice APIs

# Thanks
Special thanks to Filipe Silvestre and Jeremy Squier for working on the *[Python server code](https://github.com/TeleSign/voice_server_demo)* that Lan Quan and I used to implement this project. 

# Block Fraudulent Callers
Using TeleSign's powerful new Voice API and the Score API, you can combine them to block scammers from calling your number. 

# How it Works
A call will come in to your server at the virtual number you bought from TeleSign. The code for "def inbound_ivr_flow(request)" will start running. The first thing that happens, is your phone number is taken from the event information sent to your server. This phone number is put into a request to the Score API. The Score API will evaluate whether the phone number is good or bad and give it a score. If the phone number receives a high score, in this case above 600, the number is blocked from the Interactive Voice Response (IVR) system. If the number is under 600, the caller is let into the IVR system and can then choose from a short menu of choices described using text-to-speech. 

NOTE: This project is for US-based phone numbers only. If you wish to use it for other countries, you will need to test in order to find out how phone numbers are handled, and if the country code is dropped or not (since a dropped country code will alter the score of a phone number in most cases).

# Prerequisites 
To get started implementing this project, you should:

* Be familiar with Python 3 (that's what the code sample is in)
* Have access to TeleSign's Score API - request access to this when you sign up for the Voice API 
* Have access to TeleSign's Voice API - https://info.telesign.com/Voice.html 
* Buy a virtual US telephone number using TeleSign's Phone Numbers API - https://enterprise.telesign.com/api-reference/apis/phone-numbers-api/get-started
* Have a server set up that you can give TeleSign the URL for (you give this manually to your Customer Success Manager) 

NOTE: TeleSign's legacy Voice API (https://enterprise.telesign.com/legacy-products/voice-api/overview) cannot be used for this project. 

# Instructions 

1. Download the code (voice_and_score.py).
2. Give TeleSign the exact URL that you will set up your customer server with.
3. Take the virtual phone number you bought, and in the code, change virtual_number = 'Buy a virtual number from TeleSign' to virtual_number = 'Your purchased US-based virtual number'
4. For auth_key put in the Basic Authentication version of your customer ID and API key. You can read more a bout setting up Basic Authentication here - https://enterprise.telesign.com/api-reference/authentication#basic-authentication
5. For customer_service_number and finance_department_number, put in phone numbers you want to call during a test of the code. 
6. Run your server and try it out! 
