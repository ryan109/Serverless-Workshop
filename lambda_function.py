"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import requests, time, json, socket

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to your example credit card. " \
                    "Why don't you ask me about your account information or pending transactions. " 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me your account information or pending transactions. " 
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Hope your not in too much debt. " \
                    "Have a nice day! "
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def set_url(bank_function, account):
    if bank_function == "getaccount":
        url = "accounts/%s" % account
    elif bank_function == "getpendingtrans":
        url = "accounts/%s/transactions" % account
    return url


def http_request(http_type, url):
    for i in range(5):
        try:    
            if http_type == 'GET':
                request = requests.get("https://sandbox.capitalone.co.uk/open-banking-example/" + url, verify=False)
                content = json.loads(request.content)
                if len(content) < 1:
                    raise ValueError("Invalid response")
                return json.loads(request.content)
            elif http_type == 'POST':
                return 'To be implemented'
        except socket.timeout:
            print('An error occured getting a response')
        time.sleep(5)


def get_account_info(intent, session):
    session_attributes = {}
    reprompt_text = None
    account_id = 1
    http_type = 'GET'
    url = set_url("getaccount", account_id)
    account_info = http_request(http_type, url)
    account_desc = account_info['Data']['Account'][0]['Description']
    card_number = account_info['Data']['Account'][0]['Account']['Identification']
    speech_output = "This account is a " + str(account_desc.lower()) + " and the card number associated with it ends in " + str(card_number[-4:])
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def total_pending_transactions(recent_transactions):
    pending = 0
    for transac in recent_transactions:
        print(transac['Status'])
        if transac['Status'] == 'Pending':
            pending += 1
    return pending

def list_pending_transactions(intent, session):
    session_attributes = {}
    reprompt_text = None
    account_id = 1
    http_type = 'GET'
    url = set_url("getpendingtrans", account_id)
    transaction_info = http_request(http_type, url)
    recent_transactions = transaction_info['Data']['Transaction']
    transaction_count = len(recent_transactions)
    pending_count = total_pending_transactions(recent_transactions)
    speech_output = "Of the last " + str(transaction_count) + " transactions, a total of " + str(pending_count) + " are pending"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    # Dispatch to your skill's intent handlers
    if intent_name == "GetAccountInfo":
        return get_account_info(intent, session)
    elif intent_name == "ListPendingTransactions":
        return list_pending_transactions(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
