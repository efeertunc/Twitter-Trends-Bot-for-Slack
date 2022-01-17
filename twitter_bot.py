from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package
import requests
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask,Response
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

def getTrends():
    URL = 'https://twitter-trends.iamrohit.in/turkey'
    content = requests.get(URL)
    soup = BeautifulSoup(content.text, 'html.parser')
    row = soup.find('tbody')
    text = row.get_text()
    all_list = text.splitlines()

    counter = 1
    list_links = []
    k = 2

    for a in soup.find_all('a', href=True):
        linkString = a['href']
        if linkString.find('search') != -1:
            counter = counter + 1
            list_links.append(linkString)
        if counter > 30:
            break

    for i in range(32):
        del all_list[i * 2]
    del all_list[64:]
    del all_list[20:23]

    for a in list_links:
        all_list.insert(k, a)
        k = k + 3

    textSon = "\n".join(all_list)

    m = textSon.replace('Ä°', 'İ').replace('Ä±', 'ı')
    m = m.replace('Ã¼', 'ü').replace('Å', 'ş')
    m = m.replace('Ã§', 'ç').replace('Ã', 'Ç')
    m = m.replace('Ä', 'ğ').replace('Å', 'Ş')
    m = m.replace('Ã¶', 'ö')
    return m
@app.route('/get-trends',methods=['POST'])
def message_count():
    client.chat_postMessage(channel="YOUR CHANNEL ID", text=getTrends())
    return Response(),200

if __name__ == "__main__":
    app.run(debug=True)

