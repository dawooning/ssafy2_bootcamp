# -*- coding: utf-8 -*-
import re
import urllib.request

from bs4 import BeautifulSoup

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter


# OAuth & Permissions로 들어가서
# Bot User OAuth Access Token을 복사하여 문자열로 붙여넣습니다
SLACK_TOKEN = "xoxb-689308795108-689793747829-LiF7zkRWfy3lD515hZiM5frx"
# Basic Information으로 들어가서
# Signing Secret 옆의 Show를 클릭한 다음, 복사하여 문자열로 붙여넣습니다
SLACK_SIGNING_SECRET = "0972cabd0d1f4d3082ddb507d496dbec"


app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)


# 크롤링 함수 구현하기
def _crawl_portal_keywords(text):
    url_match = re.search(r'<(http.*?)(\|.*?)?>', text)
    if not url_match:
        return '올바른 URL을 입력해주세요.'

    url = url_match.group(1)
    source_code = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source_code, "html.parser")

    # 여기에 함수를 구현해봅시다.
    keywords = []
    if "naver" in url :
        for data in (soup.find_all("span", class_="ah_k")):
            if not data.get_text() in keywords :
            #10위까지만 크롤링하겠습니다.
                if len(keywords) >= 10:
                    break
                keywords.append(data.get_text())
    elif "daum" in url :
        for data in soup.find_all("a", class_="link_issue"):
            if not data.get_text() in keywords :
                keywords.append(data.get_text())

    # 키워드 리스트를 문자열로 만듭니다.
    return u'\n'.join(keywords)


# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    keywords = _crawl_portal_keywords(text)
    slack_web_client.chat_postMessage(
        channel=channel,
        text=keywords
    )


# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=4040)
