# -*- coding: utf-8 -*-

import re

import urllib.request
import json
from slack.web.classes import extract_json
from bs4 import BeautifulSoup
from flask import Flask, request, make_response, Response
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from slack.web.classes.blocks import *
from slack.web.classes.elements import *
from slack.web.classes.interactions import MessageInteractiveEvent

SLACK_TOKEN = 'xoxb-685325156311-678260131907-pVY7RsaR2mnchKuEQSjsV3ZC'
SLACK_SIGNING_SECRET = '3fe9514c67a35b4ddf08caaa78621ae2'

app = Flask(__name__)

# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

ids = [] # for 여러 번 출력 방지

# 크롤링 함수 구현하기
def _crawl_exercise(parts, channel):
    titles = []
    links = []
    thumb_urls = []

    if parts == "전신":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EC%A0%84%EC%8B%A0%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    elif parts == "복부":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EB%B3%B5%EB%B6%80%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    elif parts == "허리":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%ED%97%88%EB%A6%AC%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    elif parts == "등":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EB%93%B1%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    elif parts == "가슴":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EA%B0%80%EC%8A%B4%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    elif parts == "어깨":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EC%96%B4%EA%B9%A8%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    elif parts == "허벅지":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%ED%97%88%EB%B2%85%EC%A7%80%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    elif parts == "종아리":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EC%A2%85%EC%95%84%EB%A6%AC%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    elif parts == "엉덩이":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EC%97%89%EB%8D%A9%EC%9D%B4%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    elif parts == "팔":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%ED%8C%94%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    elif parts == "목":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EB%AA%A9%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    elif parts == "손목":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EC%86%90%EB%AA%A9%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    elif parts == "발목":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EB%B0%9C%EB%AA%A9%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    elif parts == "고관절":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EA%B3%A0%EA%B4%80%EC%A0%88%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    elif parts == "무릎":
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EB%AC%B4%EB%A6%8E%EC%9A%B4%EB%8F%99'
        titles, links, thumb_urls = _crawl_parts(url)

    thumbnail_block = ImageBlock(
        image_url=thumb_urls[0],
        alt_text="이미지 로드 실패"
    )

    link_block = SectionBlock(
        text=titles[0] + "\n" + links[0] + "\n"
    )

    thumbnail_block2 = ImageBlock(
        image_url=thumb_urls[1],
        alt_text="이미지 로드 실패"
    )

    link_block2 = SectionBlock(
        text=titles[1] + "\n" + links[1] + "\n"
    )

    thumbnail_block3 = ImageBlock(
        image_url=thumb_urls[2],
        alt_text="이미지 로드 실패"
    )

    link_block3 = SectionBlock(
        text=titles[2] + "\n" + links[2] + "\n"
    )

    myBlocks = [thumbnail_block, link_block, thumbnail_block2, link_block2, thumbnail_block3, link_block3]
    slack_web_client.chat_postMessage(
        channel=channel,
        text=parts + " 운동 결과입니다.",
        attachments=[{"blocks": extract_json(myBlocks)}],
    )

# 운동 크롤링
def _crawl_parts(url):
    source_code = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source_code, "html.parser")

    thumbnail_urls = [url.find("img")["src"] for url in soup.find_all("div", class_="lesson_thumb")]
    links = [link.find("a")["href"] for link in soup.find_all("div", class_="dti_sec")]
    titles = []

    for link in links:
        url = link
        source_code = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(source_code, "html.parser")
        titles.append(soup.find("div", class_="watch_title").find("h3").get_text())

    return [titles, links, thumbnail_urls]

# 안내 메시지 출력
def _display_guide(channel):
    guide = "안녕하세요.\n당신의 건강을 책임지는 핏봇 입니다.\n'@<봇이름> 메뉴'와 같이 멘션하여 매뉴얼을 확인해주세요."

    guide_block = SectionBlock(text=guide)
    block = [guide_block]

    slack_web_client.chat_postMessage(
        channel=channel,
        attachments=[{"blocks": extract_json(block)}],
    )


# 매뉴얼 출력
def _display_manual(channel):
    menu = "목적에 따라 아래와 같이 멘션해주세요.\n\n" \
           + "1. 부위별 운동방법: @<봇이름> 운동\n" \
           + "2. 소모 칼로리 계산: @<봇이름> 칼로리\n" \
           + "3. 다이어트 식단: @<봇이름> 식단"

    menu_block = SectionBlock(text=menu)
    block = [menu_block]

    slack_web_client.chat_postMessage(
        channel=channel,
        attachments=[{"blocks": extract_json(block)}],
    )


# 칼로리 출력
def _display_calory(channel):
    img_url = 'https://postfiles.pstatic.net/MjAxOTA3MTJfMTMg/MDAxNTYyODkxNDUwNjQ5.k0Oqa8Oidfv9UySXLmMKeEjDX_ZYuqUOnCkj_CFzEjkg.oMtkknq0R72ckBuzisNLiLdod_tlp-KktGufNBvqR_sg.PNG.dj5427/칼로리.PNG?type=w773'
    link = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=칼로리+계산기&oquery=운동&tqi=UfNIPlprvOsssAslOGKssssst6d-422061"

    link_block = SectionBlock(text=link)
    img_block = ImageBlock(
        image_url=img_url,
        alt_text="이미지 로드 실패"
    )
    block = [img_block, link_block]

    slack_web_client.chat_postMessage(
        channel=channel,
        attachments=[{"blocks": extract_json(block)}],
    )


# 다이어트 식단 링크 출력
def _display_diet(channel):
    url = 'http://www.10000recipe.com/recipe/list.html?q=%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8'
    source_code = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source_code, "html.parser")

    img_url = soup.find("div", class_="gnb_top").find("img")["src"]
    link = "http://www.10000recipe.com/recipe/list.html?q=다이어트"

    link_block = SectionBlock(text=link)
    img_block = ImageBlock(
        image_url=img_url,
        alt_text="이미지 로드 실패"
    )
    block = [img_block, link_block]

    slack_web_client.chat_postMessage(
        channel=channel,
        attachments=[{"blocks": extract_json(block)}],
    )


# 운동 매뉴얼 출력
def _display_exercise(channel, parts):
    message = "(전신/복부/허리/등/가슴/어깨/허벅지/종아리/엉덩이/팔/목/손목/발목/고관절/무릎)\n\n" \
              + "위에서 운동법을 알고자 하는 부위를 골라 다음과 같이 멘션해주세요.\n" \
              + "ex) '@<봇이름> 어깨'"

    message_block = SectionBlock(text=message)
    block = [message_block]

    slack_web_client.chat_postMessage(
        channel=channel,
        attachments=[{"blocks": extract_json(block)}],
    )


# 매뉴얼 안내
def _alert(channel):
    alert = "※ 매뉴얼에 따라 멘션해주세요 ※\n ('@<봇이름> 메뉴' 참고)"

    alert_block = SectionBlock(text=alert)
    block = [alert_block]

    slack_web_client.chat_postMessage(
        channel=channel,
        attachments=[{"blocks": extract_json(block)}],
    )


# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    print(event_data)

    # 중복 출력 방지
    if event_data in ids:
        return
    else:
        ids.append(event_data)

    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    menu = ["운동", "칼로리", "식단"]
    parts = ["전신", "복부", "허리", "등", "가슴", "어깨", "허벅지", "종아리", "엉덩이", "팔", "목", "손목", "발목", "고관절", "무릎"]

    print(text)

    flag = -1
    for i in range(0, len(text)):
        if text[i] == ' ':
            flag = i
            break

    if flag != -1:
        text = text[flag + 1:]

    if text == '<@UKY7N3VSP>':
        _display_guide(channel)
    elif text == '메뉴':
        _display_manual(channel)
    elif text == menu[0]:
        _display_exercise(channel, parts)
    elif text == menu[1]:
        _display_calory(channel)
    elif text == menu[2]:
        _display_diet(channel)
    elif text in parts:
        _crawl_exercise(text, channel)
    else:
        _alert(channel)

    ids.clear()

# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=4040)
