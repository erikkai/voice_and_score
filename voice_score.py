from datetime import datetime
from typing import Optional
from json import dumps
import requests

import bottle
from bottle import run, request, Bottle

application = Bottle()
headers = {
    'Content-Type': "application/json",
}
auth_key = "Your Basic Auth Key combining your customer ID and your API key"

class TelesignEvent:
    """
    Events Telesign Voice API sends.
    """
    INCOMING_CALL = "incoming_call"
    CALL_COMPLETED = "call_completed"
    CALL_LEG_COMPLETED = "call_leg_completed"
    ANSWERED = "dial_completed"
    PLAY_COMPLETED = "play_completed"
    SPEAK_COMPELTED = "speak_completed"

class DialAction:
    def __init__(self, to: str, caller_id_number: str):
        self.method: str = 'dial'
        self.parameters = {
            'to': to,
            'caller_id_number': caller_id_number,
        }

class SpeakAction:
    def __init__(self, tts_message: str, language: Optional[str]=None, collect_digits: bool=False, digits_to_collect: int=1):
        self.method: str = 'speak'
        self.parameters: dict = {
            'tts': {
                'message': tts_message,
                'language': language,
            }
        }
        if collect_digits:
            self.parameters['collect_digits'] = {
                'max': digits_to_collect,
            }

class PlayAction:
    def __init__(self, url: str, collect_digits: bool=False, digits_to_collect: int=1):
        self.method: str = 'play'
        self.parameters: dict = {
            'url': url
        }
        if collect_digits:
            self.parameters['collect_digits'] = {
                'max': digits_to_collect,
            }

class HangupAction:
    def __init__(self):
        self.method = 'hangup'
        self.parameters = {}

def generate_response(action):
    return dumps({
        'jsonrpc': '2.0',
        'method': action.method,
        'params': action.parameters
    })


@application.get('/health')
def health():
    return bottle.HTTPResponse({
        'service': 'python_customer_server',
        'description': 'endpoints for customer server',
        'pinged_on': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    })


@application.post('/')
def telesign_event():
    payload = generate_response(inbound_ivr_flow(request))
    return bottle.HTTPResponse(body=payload, headers=headers)



def inbound_ivr_flow(request):
    """
    This scenario demonstrates a customer calling into your call center.
    Through some fancy account lookup you know their name is Dave, so we can use it throughout the call.
    Dave will comb through the menu and we connect him with the appropriate department.
    """

    event = request.json.get('event')
    virtual_number = 'Buy a virtual number from TeleSign'
    customer_service_number = 'Test number like your own number'
    finance_dept_number = 'Test number like a friend's number'

    selected_digit_to_department_mapping = {
        '1': customer_service_number,
        '2': finance_dept_number,
    }

    if event == TelesignEvent.INCOMING_CALL:

        # Get the phone number of whoever is calling
        from_number = request.json['data']['from']

        # Hack to add the country code. Only for US numbers, this hack is added because the country code is being dropped out of the number
        # when sent.

        print(f"Pre-formatted number: {from_number}")
        if from_number[0] != "1" and len(from_number) == 10:
            from_number = "1" + from_number


        # Send a request to evaluate the phone number
        url = 'https://rest-ww.telesign.com/v1/score/' + from_number
        payload = "account_lifecycle_event=transact"
        headers = {
           'content-type': "application/x-www-form-urlencoded",
            # NOTE: For this you need to base64 encode customer_id:api_key and then include the resulting string in place of the entire phrase
            # base64encode(customer_id:api_key).

           'authorization': f"Basic {auth_key}"
        }
        response = requests.request("POST", url, data=payload, headers=headers)

        # Decide if you should talk to them

        if (response.json()['risk']['score'] >= 600):
            print(f"Failure score for phone number {from_number} is: {response.json()['risk']['score']}")
            ivr_message = f"Your risky score of {response.json()['risk']['score']} is too high to join this exclusive club."

            return SpeakAction(
                tts_message=ivr_message,
                language='en-US',
                collect_digits=False
            )

        else:
            print(f"Passing score for phone number {from_number} is: {response.json()['risk']['score']}")
            ivr_message = f"Your score of {response.json()['risk']['score']} is cool.  Press 1 to talk to Lan.  Press 2 to talk to Filipe."
            return SpeakAction(
                tts_message=ivr_message,
                language='en-US',
                collect_digits=True
            )

    elif event == TelesignEvent.SPEAK_COMPELTED:
        selected_department = request.json['data']['collected_digits']

        if selected_department in selected_digit_to_department_mapping:
            return DialAction(
                caller_id_number=virtual_number,
                to=selected_digit_to_department_mapping[selected_department],
            )
        elif not selected_department:
            return PlayAction(
                url="URL for the file you want to play",
                collect_digits=False
            )
        else:
            return HangupAction()

    elif event == TelesignEvent.CALL_COMPLETED:
        # Telesign does not process your response, so responding is unnecessary
        record_cdr(request.json)

    else:
        # You do not know the number
        return HangupAction()


def record_cdr(call_completed_event):
    """Store this transaction log somewhere"""
    pass

def record_survey_response(survey_response):
    pass


if __name__ == '__main__':
    run(application, host='0.0.0.0', port='8080')
