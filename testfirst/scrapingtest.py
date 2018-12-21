# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request

from formats import *

from selenium import webdriver
from operator import itemgetter
from bs4 import BeautifulSoup
from slackclient import SlackClient
from slacker import Slacker
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

#  here is token place
driver = webdriver.Chrome(r'C:\Users\student\Desktop\chromedriver_win32\chromedriver.exe')

def default_guide(text):
    '''
    디폴트 가이드
    '''
    return "This is Shopping Bot For helping your comfortable shopping!"

# 이전 검색 관련 상품 저장 리스트
product_list = [0 for i in range(10)]
pre_product = ' '
def show_best(text):
    '''
    보여줄 url을 받아와서 관련 페이지 인기상품을 리스트로 반환
    '''
    global pre_product
    if "브랜드" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain1.html"
        pre_product = "브랜드 패션"
    elif "의류" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain2.html"
        pre_product = "의류"
    elif "잡화" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain3.html"
        pre_product = "잡화"
    elif "인기" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain.html"
        pre_product = "인기"
    else:
        return "저희가 할 수 있는 영역이 아닙니다."

    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, "html.parser")
    keywords = ["11번가 " + pre_product + " 베스트 10 품목\n\n"]
    products = soup.find_all("div", class_="pup_title")
    links = []
    # product_list 초기화
    for i in range(10):
        product_list[i] = 0

    for x in products:
        links.append(x.find("a")["href"])

    for i in range(10):
        keywords.append("<" + links[i] + "|" + str(i + 1) + "위: " + products[i].get_text().strip().replace('\n', ' ') + ">\n")
        product_list[i] = links[i]

    print(keywords)
    return keywords


def show_best_price(text):
    '''
    보여줄 url을 받아와서 관련 페이지 인기상품과 가격 정보를 리스트로 반환
    '''
    global pre_product
    if "브랜드" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain1.html"
        pre_product = "브랜드"
    elif "의류" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain2.html"
        pre_product = "의류"
    elif "잡화" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain3.html"
        pre_product = "잡화"
    elif "인기" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain.html"
        pre_product = "인기"
    else:
        return "저희가 할 수 있는 영역이 아닙니다."

    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, "html.parser")
    keywords = ["11번가 " + pre_product + " 베스트 10 품목 and 가격\n\n"]

    products = soup.find_all("div", class_="pup_title")
    prices = soup.find_all("div", class_="pub_priceW")

    links = []
    for x in products:
        links.append(x.find("a")["href"])

    if "인기" in text:
        prices = prices[8:]
    else:
        prices = prices[4:]

    for i in range(10):
        keywords.append("<" + links[i] + "|" + str(i + 1) + "위: " + products[i].get_text().strip().replace('\n', ' ') + " | 가격: " + prices[
            i].get_text().replace('\n', ' ') + ">\n")
        product_list[i] = links[i]

    return keywords

# 평점 검색
def show_review(rank):
    rank = int(rank) - 1
    print("후기")
    if rank > 10:
        return "검색할 수 없는 순위입니다."
    else:
        if product_list[rank] == 0:
            return "평점이 없습니다."
        else:
            review_url = product_list[rank]
            driver.get(review_url)
            source = driver.page_source
            soup = BeautifulSoup(source, "html.parser")

            res = pre_product + "의 평점입니다. \n"
            for review in soup.find_all("span", class_="selr_star"):
                result = review.get_text().replace("판매자 평점", "구매만족도")

            result = res + result
            return result


def sorted_by_prices(text):
    '''
        가격순으로 정렬하겠음니다 zip써서 튜플로 싸서 sorted
    '''

    global pre_product
    if "브랜드" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain1.html"
        pre_product = "브랜드"
    elif "의류" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain2.html"
        pre_product = "의류"
    elif "잡화" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain3.html"
        pre_product = "잡화"
    elif "인기" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain.html"
        pre_product = "인기"
    else:
        return "저희가 할 수 있는 영역이 아닙니다."

    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, "html.parser")
    keywords = ["11번가 " + pre_product + " 를 낮은가격순으로 보여드립니다. \n\n"]

    products = soup.find_all("div", class_="pup_title")
    prices = soup.find_all("div", class_="pub_priceW")

    if "인기" in text:
        prices = prices[8:]
    else:
        prices = prices[4:]

    # sorted
    pricelist = []
    product_list = []
    sorted_list=[]

    for i in range(10):
        pricelist.append(prices[i].get_text().replace('\n', ' '))
        product_list.append(products[i].get_text().strip())

    for i in range(10):
        sorted_list.append(int(re.findall('\d+', pricelist[i])[0]))

    print(sorted_list)
    print(pricelist)
    print(product_list)
    product_price = zip(pricelist, product_list, sorted_list)

    product_price = sorted(product_price, key = lambda price:price[2])
    print(product_price)

    for i in range(10):
        keywords.append(str(i + 1) + "위: " + str(product_price[i][0]) + str(product_price[i][1])+"\n\n")

    return keywords

def sorted_by_prices_high(text):
    '''
        높은가격순으로 정렬하겠음니다 zip써서 튜플로 싸서 sorted
    '''

    global pre_product
    if "브랜드" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain1.html"
        pre_product = "브랜드"
    elif "의류" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain2.html"
        pre_product = "의류"
    elif "잡화" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain3.html"
        pre_product = "잡화"
    elif "인기" in text:
        url = "http://www.11st.co.kr/html/bestSellerMain.html"
        pre_product = "인기"
    else:
        return "저희가 할 수 있는 영역이 아닙니다."

    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, "html.parser")
    keywords = ["11번가 " + pre_product + " 를 낮은가격순으로 보여드립니다. \n\n"]

    products = soup.find_all("div", class_="pup_title")
    prices = soup.find_all("div", class_="pub_priceW")

    if text == "인기":
        prices = prices[8:]
    else:
        prices = prices[4:]

    # sorted
    pricelist = []
    product_list = []
    sorted_list=[]

    for i in range(10):
        pricelist.append(prices[i].get_text().strip().replace('\n',' '))
        product_list.append(products[i].get_text().strip())

    for i in range(10):
        sorted_list.append(int(re.findall('\d+',pricelist[i])[0]))

    print(sorted_list)
    product_price = zip(pricelist, product_list,sorted_list)

    product_price = sorted(product_price, key = lambda price:price[2],reverse=True)
    print(product_price)

    for i in range(10):
        keywords.append(str(i + 1) + "위: " + str(product_price[i][0]) + str(product_price[i][1])+"\n\n")

    return keywords


def search_product(text):
    '''
        여기에는 상품검색 기능을 넣겟음니다..
    '''
    driver.get("http://www.11st.co.kr/html/main.html")
    # 검색창 찾기
    search_text = driver.find_element_by_id("AKCKwd")
    search_text.send_keys(text[0])

    # 검색 버튼
    btn = driver.find_element_by_id("gnbTxtAd")
    btn.click()

    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    result = [" 검색결과 입니다\n\n"]
    for product in soup.find_all("div", class_="pname"):
        result.append(product.get_text().replace("\n", " ").replace("무료배송", "") + "\n")

    result = result[:11]

    return result


# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    text = re.sub(r'<@\S+> ', '', text)
    m = re.compile(r'<@\S+>')
    finddefualt = m.match(text)

    # 여기에 함수를 구현해봅시다.
    if finddefualt:
        print("디폴트실행")
        msg = format1
        result = default_guide(text)
    elif "평점" in text:
        msg = {}
        if product_list[0] == 0:
            result = "보여드릴 평점이 없습니다."
        else:
            compile_rank = re.compile('\d+')
            match = re.search(compile_rank, text)
            if (match):

                result = show_review(match.group())
            else:
                res = show_review(0)
                result = "순위를 명시하지 않아서 1위 " + pre_product + "상품의 평점입니다.\n" + res
    elif "검색" in text:
        msg = {}
        search_text = re.split("검색", text)
        result = search_product(search_text)
    elif not "가격" in text:
        print("품목실행")
        msg = {}
        result = show_best(text)
    elif "낮은가격" in text:
        msg = {}
        result = sorted_by_prices(text)
    elif "높은가격" in text:
        msg = {}
        result = sorted_by_prices_high(text)
    else:
        print("가격실행")
        msg = {}
        result = show_best_price(text)

    return (u''.join(result), msg)

pre_ts = 0
# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        global pre_ts
        if float(slack_event["event"]["ts"]) > pre_ts:
            result = _crawl_naver_keywords(text)
            pre_ts = float(slack_event["event"]["ts"])

            sc.api_call(
                "chat.postMessage",
                channel=channel,
                text=result[0],
                # if text == 'nothing':
                attachments = json.dumps([result[1]])
            )

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=3000)