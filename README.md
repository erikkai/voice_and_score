# voice_and_score
Block robocalls and other fraudulent callers by combining TeleSign's Score and Voice APIs! When a call comes in, Score evaluates the caller's phone number and decides whether to block the caller from reaching you, or let the phone number through.

# Thanks
Special thanks to Filipe Silvestre and Jeremy Squier for working on the *[Python server code](https://github.com/TeleSign/voice_server_demo)* that Lan Quan and I used to implement this project. 

# Block Fraudulent Callers
Using TeleSign's powerful new Voice API and the Score API, you can combine them to block scammers from calling your number. 

# What's in this Project
You buy a phone number from TeleSign and provide TeleSign with the URL for your server. When someone calls your designated TeleSign phone number, TeleSign routes an incoming call event to the server at the URL you provided. Your server code uses TeleSign's Score API to evaluate whether the caller should be let into the system or not. The way Score works, is it assigns a lower score to a phone number if it's a good phone number, and a higher score if the phone number seems sketchy. 

If a caller's score is low enough, the caller makes it into a mini Interactive Voice Response (IVR) system where you can choose from a menu whether to call option 1 or option 2. You can change up what's included in the system using TeleSign's Voice API documentation, provided here: https://enterprise.telesign.com/api-reference/apis/voice

# Prerequisites 
To get started implementing this project, you should:

* Be familiar with Python 3 (that's what the code sample is in)
* Have access to TeleSign's Score API - request access to this when you sign up for the Voice API 
* Have access to TeleSign's Voice API - Sign up for your trial here - https://info.telesign.com/Voice.html 
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
