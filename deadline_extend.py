
# import flask dependencies:
from flask import Flask, render_template, request, make_response, jsonify
import time
import json
import requests
import threading
import _thread
import os
import re
from datetime import datetime, timedelta

# initialize the flask app:
app = Flask(__name__)
start = ''

@app.route('/')
def index():
    return "Hello world"


def thread(text,file_name):
    print("Inside a thread.................",file_name)
    # Added time delay to fail the below 'if condition' of normal response for welcome intent:
    try:
        start_time = time.time()
        print("Text without strip============>", text)
        text = text.strip()
        print("Text===========>", text)
        req_pr = {
            "prompt": "I am an NDIS Advisor BOT powered by AI. The NDIS can provide services to all people with disability with information and connections in their communities such as doctors, sporting clubs, support groups, libraries and schools, as well as information about what support is provided by each state and territory government. I will provide you with the best response to any query you may have regarding the NDIS National Disability Insurance Scheme and its other supports like Home and Living supports, personal care supports etc. ILO (Individualised living options) is a package of supports that lets you choose where and how you live in the way that best suits you. ILO funding does not pay for a house. The purpose of ILO is for you to live in a way that best suits you. Your ILO and the funding you get will be specific to your needs. We consider your preferences, strengths, support needs, informal and community networks when deciding the right ILO funding for you. Specialist Disability Accommodation (SDA) is a range of housing designed for people with extreme functional impairment or very high needs. It aims to make accessing supports easier. SDA usually involves a shared home with a small number of other people. You might also be able to live in SDA by yourself if that option best meets your needs and circumstances. The NDIS may also provide support for temporary accommodation, including: Short Term Accommodation (STA) is periods of 14 days at a time up to 28 days, then Medium Term Accommodation (MTA) is periods of time up to 90 days.\n\nQ: How can I apply for ILO?\nA: Talk to your LAC or planner about exploring your home and living options. If you have a goal to explore the home and living options, we’ll start by getting some information from you. We’ll ask you to complete the Home and Living Supports Request form https://www.ndis.gov.au/participants/home-and-living/home-and-living-supporting-evidence-form and request a review of your plan. Based on the information in the Home and Living Supports Request Form and request for review, the NDIA will review your request and determine how much support you need to explore and design your ILO package.\n\nQ: What does it mean by self-management?\nA: Self-management support assists the participant to strengthen their abilities to self-manage their funds and supports them to build capacity to undertake all aspects of plan administration and management. This includes building organisational skills; engaging providers; enhancing the participant’s ability to direct their support; developing service agreements; building financial skills; maintaining records; paying providers; claiming payments from the NDIA.\n\nQ: "+text+"\n",
            "temperature": 0.8,
            "max_tokens": 100,
            "top_p": 1.0,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "best_of": 1,
            "model": "davinci:ft-personal-2022-07-20-05-38-31",
            "stop": ["\n"]
        }

        headers = {'Authorization': 'Bearer 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',
                   'Content-Type': 'application/json'}
        response_time = time.time()
        response = requests.post(
            'https://api.openai.com/v1/completions', headers=headers, data=json.dumps(req_pr))
        print("Time taken by response===============>",
              time.time()-response_time)
        response = response.json()
        # print(response)
        if response.get("error"):
            print("Inside IF................")
            ans_str = response["error"]["message"]
        else:
            ans_str = response.get("choices")[0].get("text")
            # print("Before removing extra text after /n =>",ans_str)
            if ans_str.find("\n") != -1:
                ans_str = ans_str.split("\n")
                ans_str = ans_str[1]
            print("response_text ====>", ans_str)
            # ans_str = ans_str.split(":")
            ans_str = ans_str[2:]
            length = len(ans_str)
            if re.findall("[?.!]$", ans_str):
                ans_str = ans_str
                print("Chekind IF condition========>", ans_str)
            else:
                for checking_sentence in range(0, len(ans_str)):
                    if re.findall("[?.!]$", ans_str):
                        print("Detected",ans_str[length-1])
                        print("length", length)
                        ans_str = ans_str[0:length]
                        break
                    else:
                        ans_str = ans_str[0:length-1]
                    length -= 1
            with open(file_name, "w") as web_response:
                web_response.write(ans_str)
        end_time = time.time() - start_time
        print("Time Takem=======>", end_time)
        return web_response
        # print("Time taken to execute thread=====>", time.time()-start_time)

    except Exception as e:
        print("Exception ==> ", e)
        return {"fulfillmentText": "Sorry, Server doesn't respond..!!",
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                "Sorry, Server doesn't respond..!!"
                            ]
                        }
                    }
                ]
                }

# _thread.start_new_thread(web_response,())


def web_response():
    
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    text = req.get('queryResult').get('queryText')
    file_name = req.get('session')
    file_name = file_name.split("/")
    # import uuid
    # file_name = uuid.uuid4()
    print(file_name)
    file_name = str(file_name[-1]) + ".txt"

    print(action, ".........................................",file_name)
    print("Checking...............")
    # time.sleep(3)
# if current time is less than or equal to extended time then only below condition becomes "True":
    if action == 'input.unknown':
        print(">>>>>>>>>>>>>>>>>>>>>>>.")
        # _thread.start_new_thread(tread,())
        _thread.start_new_thread(thread, (text,file_name))
        # logging.info("Main    : before running thread")
        # x.start()
        # try:
        #     import os
        #     os.remove(file_name)
        # except Exception as e:
        #     print("Exception ==> ", e)

        time.sleep(3)
        print("enter into first followup event")
        try:
            with open(file_name, "r")as response:
                web_response = response.read()
                print("Response from first followup event===>", web_response)
        except:
            web_response = ""

        if web_response:
            # print("Response==============++++++++===========>", web_response)
            # make a webhook response for welcome intent:
            reply = {"fulfillmentText": web_response,
                     "fulfillmentMessages": [
                         {
                             "text": {
                                 "text": [
                                     web_response
                                 ]
                             }
                         }
                     ],
                     }
            import os
            os.remove(file_name)

        else:
            print("???????????????????????")
            # Create a Followup event when above "if condition" fail:
            reply = {
                "followupEventInput": {
                    "name": "extent_webhook_deadline",
                    "languageCode": "en-US"
                }
            }

    # Create a chain of followup event. Enter into first follow up event:
    # second intent action:
    if action == 'followupevent':
        print("enter into first followup event")

        # Added time delay to fail the below 'if condition' and extend time by "3.5 sec", means right now total time "7 seconds" after webhook execute:
        time.sleep(3)
        try:
            with open(file_name, "r")as response:
                web_response = response.read()
                print("Response from secound followup event", web_response)
        except:
            web_response = ""
        # if current time is less than or equal to extended time then only below condition becomes "True":
        if web_response:
            # print("Response===============>", web_response)
            # make a webhook response for welcome intent:
            reply = {"fulfillmentText": web_response,
                     "fulfillmentMessages": [
                         {
                             "text": {
                                 "text": [
                                     web_response
                                 ]
                             }
                         }
                     ],
                     }
            import os
            os.remove(file_name)

        else:
            print("????????????????????")
            # Create a Followup event when above "if condition" fail:
            reply = {
                "followupEventInput": {
                    "name": "extent_webhook_deadline",
                    "languageCode": "en-US"
                }
            }

    # Third intent action:
    if action == 'followupevent_2':
        print("enter into second followup event")

        # Added time delay to fail the below condition and extended more time by "3.5 sec", means right now total time "3.50.5 seconds" after webhook execute:
        time.sleep(3.5)

        # below resonse should be generated for extended webhook deadline:
        try:
            with open(file_name, "r")as response:
                web_response = response.read()
                print("Response from first followup event", web_response)
        except:
            web_response = ""
        # if current time is less than or equal to extended time then only below condition becomes "True":
        if web_response:
            # make a webhook response for welcome intent:
            reply = {"fulfillmentText": web_response,
                     "fulfillmentMessages": [
                         {
                             "text": {
                                 "text": [
                                     web_response
                                 ]
                             }
                         }
                     ],
                     }
            import os
            os.remove(file_name)

        else:
            print("????????????????????")
            # Create a Followup event when above "if condition" fail:
            reply = {
                "followupEventInput": {
                    "name": "extent_webhook_deadline",
                    "languageCode": "en-US"
                }
            }

        # print("Final time of execution:=>", now.strftime("%H:%M:%S"))

    return reply

# create a route for webhook: =>   example:http://localhost:5000/webhook


@app.route('/gpt3-api-bypass', methods=['GET', 'POST'])
def webhook():

    # return response
    return make_response(jsonify(web_response()))


# run the app
if __name__ == '__main__':
    app.run(debug=True, port=33507)
