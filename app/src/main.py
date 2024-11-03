# -*- coding: utf-8 -*-
# flutter pub add serious_python
# dart run serious_python:main package app/src -p Windows --requirements -r,app/src/requirements.txt


#set SERIOUS_PYTHON_SITE_PACKAGES=$(pwd)/build/site-packages
#export SERIOUS_PYTHON_SITE_PACKAGES=$(pwd)/build/site-packages
#dart run serious_python:main package app\src -p Android --requirements -r,app\src\requirements.txt

######################################
##      카드 법인 보유내역 조회
######################################


import requests, json, base64
import urllib
import os
from datetime import datetime

# ========== HTTP 기본 함수 ==========

def http_sender(url, token, body):
    headers = {'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
        }

    response = requests.post(url, headers = headers, data = urllib.parse.quote(str(json.dumps(body))))

    #print('response.status_code = ' + str(response.status_code))
    #print('response.text = ' + urllib.parse.unquote_plus(response.text))

    return response
# ========== HTTP 함수  ==========

# ========== Toekn 재발급  ==========
def request_token(url, client_id, client_secret):
    authHeader = stringToBase64(client_id + ':' + client_secret).decode("utf-8")
    body = 'grant_type=client_credentials&scope=read'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + authHeader
        }

    response = requests.post(url, data = body, headers = headers)

    #print(response.status_code)
    #print(response.text)

    return response
# ========== Toekn 재발급  ==========

# ========== Encode string data  ==========
def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')
# ========== Encode string data  ==========

# CodefURL
token_url = 'https://oauth.codef.io/oauth/token'
codef_url = 'https://development.codef.io'

DEMO_CLIENT_ID 	= '6d7aa356-b813-4750-ab18-47231c000137'        # CODEF 클라이언트 아이디
DEMO_SECERET_KEY 	= '3782d6e9-ef56-4a10-9750-4c4b1f668287'    # CODEF 클라이언트 시크릿

# 카드 개인 보유내역 조회
card_list_path = '/v1/kr/card/p/account/card-list'
#카드 승인내역 조회
card_approval_path = '/v1/kr/card/p/account/approval-list'
#카드 혜택 조회
card_benefit_path = '/v1/kr/card/p/account/result-check-list'

# 기 발급된 토큰
token ='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2aWNlX3R5cGUiOiIxIiwic2NvcGUiOlsicmVhZCJdLCJzZXJ2aWNlX25vIjoiMDAwMDA0Njc5MDAyIiwiZXhwIjoxNzMxMjIyODgwLCJhdXRob3JpdGllcyI6WyJJTlNVUkFOQ0UiLCJQVUJMSUMiLCJCQU5LIiwiRVRDIiwiU1RPQ0siLCJDQVJEIl0sImp0aSI6IjQwMzZhYjIxLWY4NDktNDM1Ni04ZmU0LWJkOGE4ZGVlZDYwNSIsImNsaWVudF9pZCI6IjZkN2FhMzU2LWI4MTMtNDc1MC1hYjE4LTQ3MjMxYzAwMDEzNyJ9.fa9FBhTzgfOgz4Xxs617B9yImj2akqykeAKVxND7jvBl4ZK2mJJ9BzqXRb_mLbU38YMoUWoWFpxYfi2BSyMPN0mvE8wRkQNBXm5BqjQ97MujPoM7yq-bHLWl-qm7iTwi-P5elGTmZhYba47_RM8bZQ3YancptSNgXLt72E578PlB2Df82yFqSltNJEgDgMiucsaumCptLLV3vXwnFJlA_Lyv0JxNqE9wd94LoTUY2Zbm2jvXnnL8im3levqbF0vjlBSxOgtfCBD9nOwLlxLHKn7W27E6dgALxXW_NL2jOusimP0E6hLyGDiKfonwAgX79nGIqClH-BmMY3AXNiDfhw'


parcedData = []
parcedData_ALL = []

  # KB카드 0301
  # 우리카드 0309
  # 현대카드 0302
  # 롯데카드 0311
  # 삼성카드 0303
  # 하나카드 0313
  # NH카드 0304
  # 전북카드 0315
  # BC카드 0305
  # 광주카드 0316
  # 신한카드 0306
  # 수협카드 0320
  # 씨티카드 0307
  # 제주카드 0321
  # 산업은행카드 0002


# # ========== 보유카드 받아오기 =============
# # BodyData#NH
# body_NH = {
#     'organization':'0304',
#     'connectedId':'TkZjTd-49UaY-bunx-hZ6',
#     'inquiryType': '1'
# }
# # BodyData#현대
# body_HD = {
#       'organization': '0302',
#       'connectedId': 'fez9B-AvA3F8c0p3nsIKiF',
#       'inquiryType': '1'
# }
# #통신용 토큰 발급 #발급 시 1주일간 유효. request마다 토큰을 발급하면 퍼포먼스는 떨어지지만 보안성에서는 더 낫지 않을까....
# response_oauth = request_token(token_url, DEMO_CLIENT_ID, DEMO_SECERET_KEY)
# if response_oauth.status_code == 200:
#     dict = json.loads(response_oauth.text)
#     token = dict['access_token']
#     print(token)

# else:
#     print('토큰발급 오류')

# # request codef_api
# response_codef_api_NH = http_sender(codef_url + card_list_path, token, body_NH)
# if response_codef_api_NH.status_code == 200: #success
#     dict_NH = json.loads(urllib.parse.unquote_plus(response_codef_api_NH.text))
#     print(dict_NH)
#     if 'data' in dict_NH and str(dict_NH['data']) != '{}':
#         print('농협 보유카드 조회 정상 처리')
#         #parcedDataTemp = dict_NH['data']
#         parcedData = dict_NH['data']
#         #parcedData = [x for x in parcedDataTemp if '본인' in x['resCardType']]
#         #print(parcedData)
#     else:
#         print('조회 오류')

# # request codef_api
# response_codef_api_HD = http_sender(codef_url + card_list_path, token, body_HD)
# if response_codef_api_HD.status_code == 200: #success
#     dict_HD = json.loads(urllib.parse.unquote_plus(response_codef_api_HD.text))
#     if 'data' in dict_HD and str(dict_HD['data']) != '{}':
#         print('현대 보유카드 조회 정상 처리')
#         parcedData.append(dict_HD['data'])
#     else:
#         print('조회 오류')
# #임시폴더에 파일 저장
# result_filename = os.getenv("RESULT_FILENAME")
# if not result_filename:
#     result_filename = "output.text"
#     #parcedData="경로에러!!!"

# parcedData_ALL.append(parcedData)

# # ========== 보유카드 받아오기 =============

# # ========== 카드 혜택 받아오기 =============
# # BodyData#NH
# body_NH = {
#     'organization':'0304',
#     'connectedId':'TkZjTd-49UaY-bunx-hZ6',
# }
# # BodyData#현대
# body_HD = {
#       'organization': '0302',
#       'connectedId': 'fez9B-AvA3F8c0p3nsIKiF',
# }

# # request codef_api
# response_codef_api_NH = http_sender(codef_url + card_benefit_path, token, body_NH)
# if response_codef_api_NH.status_code == 200: #success
#     dict_NH = json.loads(urllib.parse.unquote_plus(response_codef_api_NH.text))
#     #print(dict_NH)
#     if 'data' in dict_NH and str(dict_NH['data']) != '{}':
#         print('농협카드 혜택조회 정상 처리')
#         parcedData = (dict_NH['data'])
#         #print(parcedData_NH)
#     else:
#         print('조회 오류')
# # request codef_api
# response_codef_api_HD = http_sender(codef_url + card_benefit_path, token, body_HD)
# if response_codef_api_HD.status_code == 200: #success
#     dict_HD = json.loads(urllib.parse.unquote_plus(response_codef_api_HD.text))
#     #print(dict_HD)
#     if 'data' in dict_HD and str(dict_HD['data']) != '{}':
#         print('현대카드 혜택조회 정상 처리')
#         parcedData.append(dict_HD['data'])
#         #print(parcedData_HD)
#     else:
#         print('조회 오류')

# parcedData_ALL.append(parcedData)

# # ========== 카드 혜택 받아오기 =============

# # ========== 카드 승인내역 받아오기 =============
# end_date = datetime.today().strftime("%Y%m%d")

# #농협카드 1분기 승인내역
# body_NH_1qt = {
#     "organization": "0304",
#     'connectedId':'TkZjTd-49UaY-bunx-hZ6',
#     "startDate": "20240101",
#     "endDate": "20240331",
#     "orderBy": "0",
#     "inquiryType": "1",
#     "cardName":"0",
# }
# #농협카드 2분기 승인내역
# body_NH_2qt = {
#     "organization": "0304",
#     'connectedId':'TkZjTd-49UaY-bunx-hZ6',
#     "startDate": "20240401",
#     "endDate": "20240630",
#     "orderBy": "0",
#     "inquiryType": "1",
#     "cardName":"0",
# }
# #농협카드 3분기 승인내역
# body_NH_3qt = {
#     "organization": "0304",
#     'connectedId':'TkZjTd-49UaY-bunx-hZ6',
#     "startDate": "20240701",
#     "endDate": "20240930",
#     "orderBy": "0",
#     "inquiryType": "1",
#     "cardName":"0",
# }
# #농협카드 4분기 승인내역
# body_NH_4qt = {
#     "organization": "0304",
#     'connectedId':'TkZjTd-49UaY-bunx-hZ6',
#     "startDate": "20241001",
#     "endDate": end_date,
#     "orderBy": "0",
#     "inquiryType": "1",
#     "cardName":"0",
# }

# # 1분기 농협카드 요청
# response_codef_api_NH = http_sender(codef_url + card_approval_path, token, body_NH_1qt)
# if response_codef_api_NH.status_code == 200: #success
#     dict_NH = json.loads(urllib.parse.unquote_plus(response_codef_api_NH.text))
#     #print(dict_NH)
#     if 'data' in dict_NH and str(dict_NH['data']) != '{}':
#         print('농협카드 1분기 승인내역 조회 정상 처리')
#         parcedDataTemp = (dict_NH['data'])
#         parcedData = [x for x in parcedDataTemp if '농협' in x['resMemberStoreName'] or '이지웰' in x['resMemberStoreName']]
#         #print(parcedData_NH)
#     else:
#         print('조회 오류')

# # 2분기 농협카드 요청
# response_codef_api_NH = http_sender(codef_url + card_approval_path, token, body_NH_2qt)
# if response_codef_api_NH.status_code == 200: #success
#     dict_NH = json.loads(urllib.parse.unquote_plus(response_codef_api_NH.text))
#     #print(dict_NH)
#     if 'data' in dict_NH and str(dict_NH['data']) != '{}':
#         print('농협카드 2분기 승인내역 조회 정상 처리')
#         parcedDataTemp = (dict_NH['data'])
#         parcedDataTemp = [x for x in parcedDataTemp if '농협' in x['resMemberStoreName'] or '이지웰' in x['resMemberStoreName']]
#         parcedData.append(parcedDataTemp)
#         #print(parcedData_NH)
#     else:
#         print('조회 오류')

# # 3분기 농협카드 요청
# response_codef_api_NH = http_sender(codef_url + card_approval_path, token, body_NH_3qt)
# if response_codef_api_NH.status_code == 200: #success
#     dict_NH = json.loads(urllib.parse.unquote_plus(response_codef_api_NH.text))
#     #print(dict_NH)
#     if 'data' in dict_NH and str(dict_NH['data']) != '{}':
#         print('농협카드 3분기 승인내역 조회 정상 처리')
#         parcedDataTemp = (dict_NH['data'])
#         parcedDataTemp = [x for x in parcedDataTemp if '농협' in x['resMemberStoreName'] or '이지웰' in x['resMemberStoreName']]
#         parcedData.append(parcedDataTemp)
#     else:
#         print('조회 오류')

# # 4분기 농협카드 요청
# response_codef_api_NH = http_sender(codef_url + card_approval_path, token, body_NH_4qt)
# if response_codef_api_NH.status_code == 200: #success
#     dict_NH = json.loads(urllib.parse.unquote_plus(response_codef_api_NH.text))
#     #print(dict_NH)
#     if 'data' in dict_NH and str(dict_NH['data']) != '{}':
#         print('농협카드 4분기 승인내역 조회 정상 처리')
#         parcedDataTemp = (dict_NH['data'])
#         parcedDataTemp = [x for x in parcedDataTemp if '농협' in x['resMemberStoreName'] or '이지웰' in x['resMemberStoreName']]
#         parcedData.append(parcedDataTemp)
#     else:
#         print('조회 오류')

# parcedData_ALL.append(parcedData)

    #임시폴더에 파일 저장
result_filename = os.getenv("RESULT_FILENAME")
if not result_filename:
    result_filename = "output.text"
    #parcedData_ALL="경로에러!!!"

parcedData_ALL = [
                    [
                        {
                            "resCardName": "채움패밀리카드Ⅱ",
                            "resCardNo": "524140******7183",
                            "resCardType": "본인",
                            "resUserNm": "김동한",
                            "resSleepYN": "N",
                            "resTrafficYN": "유",
                            "resValidPeriod": "20***1",
                            "resIssueDate": "20240912",
                            "resImageLink": "https://card.nonghyup.com/content/imgs/shopmall/pro_img/card/N10034.png",
                            "resState": "정상"
                        },
                        {
                            "resCardName": "채움패밀리카드Ⅱ",
                            "resCardNo": "524140******7183",
                            "resCardType": "가족",
                            "resUserNm": "김재남",
                            "resSleepYN": "N",
                            "resTrafficYN": "유",
                            "resValidPeriod": "20***1",
                            "resIssueDate": "20240912",
                            "resImageLink": "https://card.nonghyup.com/content/imgs/shopmall/pro_img/card/N10034.png",
                            "resState": "정상"
                        },
                        {
                            "resCardName": "K-패스카드(채움)_체크",
                            "resCardNo": "485479******7482",
                            "resCardType": "본인",
                            "resUserNm": "김동한",
                            "resSleepYN": "N",
                            "resTrafficYN": "유",
                            "resValidPeriod": "20***3",
                            "resIssueDate": "20240426",
                            "resImageLink": "https://card.nonghyup.com/content/imgs/shopmall/pro_img/card/F20517.png",
                            "resState": "DCC 해외원화결제 차단"
                        },
                        {
                            "resCardName": "NH1934 체크카드",
                            "resCardNo": "546111******0613",
                            "resCardType": "본인",
                            "resUserNm": "김동한",
                            "resSleepYN": "N",
                            "resTrafficYN": "무",
                            "resValidPeriod": "20***2",
                            "resIssueDate": "20220112",
                            "resImageLink": "https://card.nonghyup.com/content/imgs/shopmall/pro_img/card/F20001.png",
                            "resState": "DCC 해외원화결제 차단"
                        },
                        {
                            "resCardName": "네이버 현대카드",
                            "resCardNo": "4***********320*",
                            "resCardType": "VISA",
                            "resUserNm": "",
                            "resSleepYN": "N",
                            "resTrafficYN": "",
                            "resValidPeriod": "",
                            "resIssueDate": "",
                            "resImageLink": "https://www.hyundaicard.com/img/com/card/029183DS_h.png",
                            "resState": ""
                        }
                    ],
                    [
                        {
                            "resCardName": "채움패밀리카드Ⅱ",
                            "resCardNo": "524140******7183",
                            "resCardType": "",
                            "resCardCompany": "",
                            "resLnkUrl": "",
                            "resCardBenefitList": [
                                {
                                    "resType": "",
                                    "resCardBenefitName": "[2030 Pack] 이동통신 요금 5% 청구할인",
                                    "resBusinessTypes": "통신",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "323050",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "[2030 Pack] 패밀리레스토랑 20% 청구할인",
                                    "resBusinessTypes": "외식",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "323050",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "[2030 Pack] 커피, 서적 50% 청구할인",
                                    "resBusinessTypes": "교육,외식",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "323050",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "[2030 Pack] 영화, 프로스포츠 50% 청구할인",
                                    "resBusinessTypes": "여가",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "323050",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "[2030 Pack] 쇼핑업종 3% NH포인트 적립",
                                    "resBusinessTypes": "쇼핑",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "323050",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "놀이공원 자유이용권 또는 입장료 할인 (20만원)",
                                    "resBusinessTypes": "여가",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "323050",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "Hi비타민 서비스",
                                    "resBusinessTypes": "기타",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "웰페어클럽서비스",
                                    "resBusinessTypes": "기타",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "대중교통 요금 5% 청구할인",
                                    "resBusinessTypes": "일상",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "323050",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "이천 청학서당 10% 할인",
                                    "resBusinessTypes": "교육",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "골프제휴 서비스(일부)_엑스골프",
                                    "resBusinessTypes": "골프",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "NH한삼인 10% 청구할인(패밀리)",
                                    "resBusinessTypes": "쇼핑",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "전 요식업종 3% 포인트 적립",
                                    "resBusinessTypes": "외식",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "323050",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "모든 주유(충전)소 3% 포인트 적립",
                                    "resBusinessTypes": "주유",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "323050",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "쇼핑서비스 대상가맹점 2~3개월 무이자 할부",
                                    "resBusinessTypes": "쇼핑",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "323050",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "브랜드서비스(마스타_티타늄)",
                                    "resBusinessTypes": "전 가맹점",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "한드레시아 이용시 15~20% 현장할인",
                                    "resBusinessTypes": "여성",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "LG패션 브랜드 최고 20% 현장할인",
                                    "resBusinessTypes": "쇼핑",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "호텔 발레파킹 무료이용_MasterCard Platinum",
                                    "resBusinessTypes": "여가",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "인천공항 발레파킹 무료이용_MasterCard Platinum",
                                    "resBusinessTypes": "항공",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "인천/김포/김해공항 라운지 무료이용_MasterCard Platinum",
                                    "resBusinessTypes": "항공",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                }
                            ]
                        },
                        {
                            "resCardName": "채움패밀리카드Ⅱ",
                            "resCardNo": "524140******7183",
                            "resCardType": "",
                            "resCardCompany": "",
                            "resLnkUrl": "",
                            "resCardBenefitList": [
                                {
                                    "resType": "",
                                    "resCardBenefitName": "[4050 Pack] 의료업종 10% 청구할인",
                                    "resBusinessTypes": "일상",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "200000",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "[4050 Pack] 골프장(연습장) 5% 청구할인",
                                    "resBusinessTypes": "골프",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "200000",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "[4050 Pack] 쇼핑업종 5% NH포인트 적립",
                                    "resBusinessTypes": "쇼핑",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "200000",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "놀이공원 자유이용권 또는 입장료 할인 (20만원)",
                                    "resBusinessTypes": "여가",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "200000",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "Hi비타민 서비스",
                                    "resBusinessTypes": "기타",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "웰페어클럽서비스",
                                    "resBusinessTypes": "기타",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "대중교통 요금 5% 청구할인",
                                    "resBusinessTypes": "일상",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "200000",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "이천 청학서당 10% 할인",
                                    "resBusinessTypes": "교육",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "골프제휴 서비스(일부)_엑스골프",
                                    "resBusinessTypes": "골프",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "NH한삼인 10% 청구할인(패밀리)",
                                    "resBusinessTypes": "쇼핑",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "전 요식업종 3% 포인트 적립",
                                    "resBusinessTypes": "외식",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "200000",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "모든 주유(충전)소 3% 포인트 적립",
                                    "resBusinessTypes": "주유",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "200000",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "쇼핑서비스 대상가맹점 2~3개월 무이자 할부",
                                    "resBusinessTypes": "쇼핑",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "200000",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "브랜드서비스(마스타_티타늄)",
                                    "resBusinessTypes": "전 가맹점",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "한드레시아 이용시 15~20% 현장할인",
                                    "resBusinessTypes": "여성",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "LG패션 브랜드 최고 20% 현장할인",
                                    "resBusinessTypes": "쇼핑",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "호텔 발레파킹 무료이용_MasterCard Platinum",
                                    "resBusinessTypes": "여가",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "인천공항 발레파킹 무료이용_MasterCard Platinum",
                                    "resBusinessTypes": "항공",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "인천/김포/김해공항 라운지 무료이용_MasterCard Platinum",
                                    "resBusinessTypes": "항공",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                }
                            ]
                        },
                        {
                            "resCardName": "K-패스카드(채움)_체크",
                            "resCardNo": "485479******7482",
                            "resCardType": "",
                            "resCardCompany": "",
                            "resLnkUrl": "",
                            "resCardBenefitList": [
                                {
                                    "resType": "",
                                    "resCardBenefitName": "모빌리티 서비스(버스/지하철 10%, 렌터카/카쉐어링/",
                                    "resBusinessTypes": "일상",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "188200",
                                            "resRequiredPerformanceAmt": "11800",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "(알뜰교통) 라이프 서비스 5% 할인(이동통신요금)",
                                    "resBusinessTypes": "통신",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "188200",
                                            "resRequiredPerformanceAmt": "11800",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "(알뜰교통) 커피전문점 5% 할인",
                                    "resBusinessTypes": "외식",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "188200",
                                            "resRequiredPerformanceAmt": "11800",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "(알뜰교통) 편의점 5% 할인",
                                    "resBusinessTypes": "일상",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "200000",
                                            "resCurrentUseAmt": "188200",
                                            "resRequiredPerformanceAmt": "11800",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                }
                            ]
                        },
                        {
                            "resCardName": "NH1934 체크카드",
                            "resCardNo": "546111******0613",
                            "resCardType": "",
                            "resCardCompany": "",
                            "resLnkUrl": "",
                            "resCardBenefitList": [
                                {
                                    "resType": "",
                                    "resCardBenefitName": "국내외 전 가맹점 0.2% 청구할인(BAZIC 체크, 매일)",
                                    "resBusinessTypes": "전 가맹점",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "국내 전 가맹점 0.3% 청구할인(BAZIC 체크, 일요일)",
                                    "resBusinessTypes": "전 가맹점",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "500000",
                                            "resCurrentUseAmt": "38210",
                                            "resRequiredPerformanceAmt": "461790",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "국내외 전 가맹점 0.2% 청구할인(BAZIC 체크, 매일, 하이브리드 보정용)",
                                    "resBusinessTypes": "전 가맹점",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "국내 전 가맹점 0.3% 청구할인(BAZIC 체크, 일요일)",
                                    "resBusinessTypes": "전 가맹점",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "500000",
                                            "resCurrentUseAmt": "38210",
                                            "resRequiredPerformanceAmt": "461790",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "SMS 휴대폰 바로 알림 서비스 무료 제공",
                                    "resBusinessTypes": "금융",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "",
                                    "resCardBenefitName": "SMS 발송(2만원이상건 시 발송)",
                                    "resBusinessTypes": "금융",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "1",
                                            "resStandardUseAmt": "0",
                                            "resCurrentUseAmt": "0",
                                            "resRequiredPerformanceAmt": "0",
                                            "commStartDate": "",
                                            "commEndDate": "",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                }
                            ]
                        },
                        {
                            "resCardName": "네이버 현대카드",
                            "resCardNo": "",
                            "resCardType": "",
                            "resCardCompany": "",
                            "resLnkUrl": "",
                            "resCardBenefitList": [
                                {
                                    "resType": "이번 달 네이버플러스 멤버십 무료이용권 제공 및 네이버페이 포인트 최대 5% 적립",
                                    "resCardBenefitName": "",
                                    "resBusinessTypes": "",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "300000",
                                            "resCurrentUseAmt": "597928",
                                            "resRequiredPerformanceAmt": "250300",
                                            "commStartDate": "20241001",
                                            "commEndDate": "20241031",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "다음 달 네이버플러스 멤버십 무료이용권 제공 및 네이버페이 포인트 최대 5% 적립",
                                    "resCardBenefitName": "",
                                    "resBusinessTypes": "",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "300000",
                                            "resCurrentUseAmt": "49700",
                                            "resRequiredPerformanceAmt": "250300",
                                            "commStartDate": "20241101",
                                            "commEndDate": "20241130",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "이번 달 일반가맹점 결제 시 네이버페이 포인트 1% 적립",
                                    "resCardBenefitName": "",
                                    "resBusinessTypes": "",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "300000",
                                            "resCurrentUseAmt": "597928",
                                            "resRequiredPerformanceAmt": "250300",
                                            "commStartDate": "20241001",
                                            "commEndDate": "20241031",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                },
                                {
                                    "resType": "다음 달 일반가맹점 결제 시 네이버페이 포인트 1% 적립",
                                    "resCardBenefitName": "",
                                    "resBusinessTypes": "",
                                    "resCardPerformanceList": [
                                        {
                                            "resMeetPerformanceYN": "0",
                                            "resStandardUseAmt": "300000",
                                            "resCurrentUseAmt": "49700",
                                            "resRequiredPerformanceAmt": "250300",
                                            "commStartDate": "20241101",
                                            "commEndDate": "20241130",
                                            "resCoverageCriteria": ""
                                        }
                                    ],
                                    "resDetailList": []
                                }
                            ]
                        }
                    ],
                    [
                        {
                            "resUsedDate": "20240330",
                            "resUsedTime": "162355",
                            "resCardNo": "546111******0613",
                            "resCardNo1": "",
                            "resMemberStoreName": "(주)농협하나로유통동탄유통센터",
                            "resUsedAmount": "101020",
                            "resPaymentType": "3",
                            "resInstallmentMonth": "",
                            "resApprovalNo": "52548993",
                            "resPaymentDueDate": "",
                            "resMemberStoreCorpNo": "",
                            "resMemberStoreType": "",
                            "resMemberStoreAddr": "",
                            "resMemberStoreTelNo": "",
                            "resAccountCurrency": "KRW",
                            "resHomeForeignType": "1",
                            "resCancelYN": "0",
                            "resCancelAmount": "",
                            "resVAT": "",
                            "resCashBack": "",
                            "resKRWAmt": "",
                            "resMemberStoreNo": "155894811",
                            "resCardName": "",
                            "commStartDate": "20240101",
                            "commEndDate": "20240331"
                        },
                        {
                            "resUsedDate": "20240313",
                            "resUsedTime": "185341",
                            "resCardNo": "245",
                            "resCardNo1": "",
                            "resMemberStoreName": "의왕농협포일지점",
                            "resUsedAmount": "9190",
                            "resPaymentType": "1",
                            "resInstallmentMonth": "",
                            "resApprovalNo": "42302963",
                            "resPaymentDueDate": "",
                            "resMemberStoreCorpNo": "",
                            "resMemberStoreType": "",
                            "resMemberStoreAddr": "",
                            "resMemberStoreTelNo": "",
                            "resAccountCurrency": "KRW",
                            "resHomeForeignType": "1",
                            "resCancelYN": "0",
                            "resCancelAmount": "",
                            "resVAT": "",
                            "resCashBack": "",
                            "resKRWAmt": "",
                            "resMemberStoreNo": "120620350",
                            "resCardName": "",
                            "commStartDate": "20240101",
                            "commEndDate": "20240331"
                        },
                        {
                            "resUsedDate": "20240301",
                            "resUsedTime": "172514",
                            "resCardNo": "546111******0613",
                            "resCardNo1": "",
                            "resMemberStoreName": "순천원예농협하나로마트",
                            "resUsedAmount": "45520",
                            "resPaymentType": "3",
                            "resInstallmentMonth": "",
                            "resApprovalNo": "43630119",
                            "resPaymentDueDate": "",
                            "resMemberStoreCorpNo": "",
                            "resMemberStoreType": "",
                            "resMemberStoreAddr": "",
                            "resMemberStoreTelNo": "",
                            "resAccountCurrency": "KRW",
                            "resHomeForeignType": "1",
                            "resCancelYN": "0",
                            "resCancelAmount": "",
                            "resVAT": "",
                            "resCashBack": "",
                            "resKRWAmt": "",
                            "resMemberStoreNo": "103042579",
                            "resCardName": "",
                            "commStartDate": "20240101",
                            "commEndDate": "20240331"
                        },
                        {
                            "resUsedDate": "20240224",
                            "resUsedTime": "151341",
                            "resCardNo": "546111******0613",
                            "resCardNo1": "",
                            "resMemberStoreName": "(주)농협하나로유통동탄유통센터",
                            "resUsedAmount": "7330",
                            "resPaymentType": "3",
                            "resInstallmentMonth": "",
                            "resApprovalNo": "62141935",
                            "resPaymentDueDate": "",
                            "resMemberStoreCorpNo": "",
                            "resMemberStoreType": "",
                            "resMemberStoreAddr": "",
                            "resMemberStoreTelNo": "",
                            "resAccountCurrency": "KRW",
                            "resHomeForeignType": "1",
                            "resCancelYN": "0",
                            "resCancelAmount": "",
                            "resVAT": "",
                            "resCashBack": "",
                            "resKRWAmt": "",
                            "resMemberStoreNo": "155894811",
                            "resCardName": "",
                            "commStartDate": "20240101",
                            "commEndDate": "20240331"
                        },
                        {
                            "resUsedDate": "20240224",
                            "resUsedTime": "151037",
                            "resCardNo": "546111******0613",
                            "resCardNo1": "",
                            "resMemberStoreName": "(주)농협하나로유통동탄유통센터",
                            "resUsedAmount": "68840",
                            "resPaymentType": "3",
                            "resInstallmentMonth": "",
                            "resApprovalNo": "62108713",
                            "resPaymentDueDate": "",
                            "resMemberStoreCorpNo": "",
                            "resMemberStoreType": "",
                            "resMemberStoreAddr": "",
                            "resMemberStoreTelNo": "",
                            "resAccountCurrency": "KRW",
                            "resHomeForeignType": "1",
                            "resCancelYN": "0",
                            "resCancelAmount": "",
                            "resVAT": "",
                            "resCashBack": "",
                            "resKRWAmt": "",
                            "resMemberStoreNo": "155894811",
                            "resCardName": "",
                            "commStartDate": "20240101",
                            "commEndDate": "20240331"
                        },
                        {
                            "resUsedDate": "20240222",
                            "resUsedTime": "145420",
                            "resCardNo": "245",
                            "resCardNo1": "",
                            "resMemberStoreName": "이지웰주식회사",
                            "resUsedAmount": "18000",
                            "resPaymentType": "1",
                            "resInstallmentMonth": "",
                            "resApprovalNo": "43496587",
                            "resPaymentDueDate": "",
                            "resMemberStoreCorpNo": "",
                            "resMemberStoreType": "",
                            "resMemberStoreAddr": "",
                            "resMemberStoreTelNo": "",
                            "resAccountCurrency": "KRW",
                            "resHomeForeignType": "1",
                            "resCancelYN": "0",
                            "resCancelAmount": "",
                            "resVAT": "",
                            "resCashBack": "",
                            "resKRWAmt": "",
                            "resMemberStoreNo": "166456630",
                            "resCardName": "",
                            "commStartDate": "20240101",
                            "commEndDate": "20240331"
                        },
                        {
                            "resUsedDate": "20240120",
                            "resUsedTime": "182615",
                            "resCardNo": "245",
                            "resCardNo1": "",
                            "resMemberStoreName": "이지웰주식회사",
                            "resUsedAmount": "510630",
                            "resPaymentType": "1",
                            "resInstallmentMonth": "",
                            "resApprovalNo": "57860031",
                            "resPaymentDueDate": "",
                            "resMemberStoreCorpNo": "",
                            "resMemberStoreType": "",
                            "resMemberStoreAddr": "",
                            "resMemberStoreTelNo": "",
                            "resAccountCurrency": "KRW",
                            "resHomeForeignType": "1",
                            "resCancelYN": "0",
                            "resCancelAmount": "",
                            "resVAT": "",
                            "resCashBack": "",
                            "resKRWAmt": "",
                            "resMemberStoreNo": "166456630",
                            "resCardName": "",
                            "commStartDate": "20240101",
                            "commEndDate": "20240331"
                        },
                        {
                            "resUsedDate": "20240119",
                            "resUsedTime": "175436",
                            "resCardNo": "245",
                            "resCardNo1": "",
                            "resMemberStoreName": "의왕농협포일지점",
                            "resUsedAmount": "7860",
                            "resPaymentType": "1",
                            "resInstallmentMonth": "",
                            "resApprovalNo": "48779001",
                            "resPaymentDueDate": "",
                            "resMemberStoreCorpNo": "",
                            "resMemberStoreType": "",
                            "resMemberStoreAddr": "",
                            "resMemberStoreTelNo": "",
                            "resAccountCurrency": "KRW",
                            "resHomeForeignType": "1",
                            "resCancelYN": "0",
                            "resCancelAmount": "",
                            "resVAT": "",
                            "resCashBack": "",
                            "resKRWAmt": "",
                            "resMemberStoreNo": "120620350",
                            "resCardName": "",
                            "commStartDate": "20240101",
                            "commEndDate": "20240331"
                        },
                        {
                            "resUsedDate": "20240115",
                            "resUsedTime": "083159",
                            "resCardNo": "245",
                            "resCardNo1": "",
                            "resMemberStoreName": "이지웰주식회사",
                            "resUsedAmount": "263050",
                            "resPaymentType": "1",
                            "resInstallmentMonth": "",
                            "resApprovalNo": "44839399",
                            "resPaymentDueDate": "",
                            "resMemberStoreCorpNo": "",
                            "resMemberStoreType": "",
                            "resMemberStoreAddr": "",
                            "resMemberStoreTelNo": "",
                            "resAccountCurrency": "KRW",
                            "resHomeForeignType": "1",
                            "resCancelYN": "0",
                            "resCancelAmount": "",
                            "resVAT": "",
                            "resCashBack": "",
                            "resKRWAmt": "",
                            "resMemberStoreNo": "166456630",
                            "resCardName": "",
                            "commStartDate": "20240101",
                            "commEndDate": "20240331"
                        },
                        [
                            {
                                "resUsedDate": "20240629",
                                "resUsedTime": "174025",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "속초농협하나로마트중앙시장점",
                                "resUsedAmount": "80570",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "49740713",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "103093617",
                                "resCardName": "",
                                "commStartDate": "20240401",
                                "commEndDate": "20240630"
                            },
                            {
                                "resUsedDate": "20240624",
                                "resUsedTime": "174826",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "의왕농협포일지점",
                                "resUsedAmount": "13700",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "73092306",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "120620350",
                                "resCardName": "",
                                "commStartDate": "20240401",
                                "commEndDate": "20240630"
                            },
                            {
                                "resUsedDate": "20240523",
                                "resUsedTime": "104037",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "27900",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "51515214",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240401",
                                "commEndDate": "20240630"
                            },
                            {
                                "resUsedDate": "20240519",
                                "resUsedTime": "142752",
                                "resCardNo": "485479******7482",
                                "resCardNo1": "",
                                "resMemberStoreName": "의왕농협포일지점",
                                "resUsedAmount": "22260",
                                "resPaymentType": "3",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "51881121",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "120620350",
                                "resCardName": "",
                                "commStartDate": "20240401",
                                "commEndDate": "20240630"
                            },
                            {
                                "resUsedDate": "20240515",
                                "resUsedTime": "144029",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주주식회사(온라인사업부)",
                                "resUsedAmount": "27900",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "50483271",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "129368424",
                                "resCardName": "",
                                "commStartDate": "20240401",
                                "commEndDate": "20240630"
                            },
                            {
                                "resUsedDate": "20240513",
                                "resUsedTime": "135503",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주(주)(축산경제)",
                                "resUsedAmount": "34500",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "67338271",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "159474060",
                                "resCardName": "",
                                "commStartDate": "20240401",
                                "commEndDate": "20240630"
                            },
                            {
                                "resUsedDate": "20240512",
                                "resUsedTime": "172649",
                                "resCardNo": "546111******0613",
                                "resCardNo1": "",
                                "resMemberStoreName": "제주남원농협하나로마트",
                                "resUsedAmount": "33970",
                                "resPaymentType": "3",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "60130660",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "103057644",
                                "resCardName": "",
                                "commStartDate": "20240401",
                                "commEndDate": "20240630"
                            },
                            {
                                "resUsedDate": "20240507",
                                "resUsedTime": "193320",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "의왕농협포일지점",
                                "resUsedAmount": "7000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "50199725",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "120620350",
                                "resCardName": "",
                                "commStartDate": "20240401",
                                "commEndDate": "20240630"
                            },
                            {
                                "resUsedDate": "20240502",
                                "resUsedTime": "134548",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주(주)(축산경제)",
                                "resUsedAmount": "60600",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "72988735",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "159474060",
                                "resCardName": "",
                                "commStartDate": "20240401",
                                "commEndDate": "20240630"
                            },
                            {
                                "resUsedDate": "20240429",
                                "resUsedTime": "163630",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "의왕농협포일지점",
                                "resUsedAmount": "28160",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "44950494",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "120620350",
                                "resCardName": "",
                                "commStartDate": "20240401",
                                "commEndDate": "20240630"
                            },
                            {
                                "resUsedDate": "20240408",
                                "resUsedTime": "144959",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "(주)농협하나로유통동탄유통센터",
                                "resUsedAmount": "620000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "62278239",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "155894811",
                                "resCardName": "",
                                "commStartDate": "20240401",
                                "commEndDate": "20240630"
                            }
                        ],
                        [
                            {
                                "resUsedDate": "20240929",
                                "resUsedTime": "203529",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "247000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "46873840",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "1",
                                "resCancelAmount": "247000",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240929",
                                "resUsedTime": "151144",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주(주)안성팜랜드분사",
                                "resUsedAmount": "25000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "43775842",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "139012594",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240929",
                                "resUsedTime": "140320",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주(주)안성팜랜드분사",
                                "resUsedAmount": "1000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "43052875",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "139012594",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240929",
                                "resUsedTime": "115450",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주(주)안성팜랜드분사",
                                "resUsedAmount": "10000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "41635870",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "139012594",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240922",
                                "resUsedTime": "190344",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "의왕농협포일지점",
                                "resUsedAmount": "9290",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "51366973",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "120620350",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240921",
                                "resUsedTime": "122403",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "의왕농협포일지점",
                                "resUsedAmount": "14200",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "76281184",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "120620350",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240918",
                                "resUsedTime": "184930",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주주식회사(온라인사업부)",
                                "resUsedAmount": "26900",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "52009306",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "129368424",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240916",
                                "resUsedTime": "164732",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "담양농협하나로마트",
                                "resUsedAmount": "22830",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "73982979",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "123196212",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240912",
                                "resUsedTime": "191416",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "8700",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "71504490",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240912",
                                "resUsedTime": "191305",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "69600",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "71491928",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240910",
                                "resUsedTime": "181530",
                                "resCardNo": "485479******7482",
                                "resCardNo1": "",
                                "resMemberStoreName": "의왕농협포일지점",
                                "resUsedAmount": "9010",
                                "resPaymentType": "3",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "50667950",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "120620350",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240909",
                                "resUsedTime": "181925",
                                "resCardNo": "485479******7482",
                                "resCardNo1": "",
                                "resMemberStoreName": "의왕농협포일지점",
                                "resUsedAmount": "2800",
                                "resPaymentType": "3",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "40137352",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "120620350",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240904",
                                "resUsedTime": "154908",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "288000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "63163843",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "1",
                                "resCancelAmount": "288000",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240830",
                                "resUsedTime": "180209",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "속초농협하나로마트중앙시장점",
                                "resUsedAmount": "3860",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "52577867",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "103093617",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240829",
                                "resUsedTime": "134528",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주(주)소매체인본부",
                                "resUsedAmount": "40000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "76199403",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "167888145",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240825",
                                "resUsedTime": "180524",
                                "resCardNo": "485479******7482",
                                "resCardNo1": "",
                                "resMemberStoreName": "송파농협하나로마트",
                                "resUsedAmount": "1460",
                                "resPaymentType": "3",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "76783121",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "144469199",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240824",
                                "resUsedTime": "161413",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "44000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "66902887",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240824",
                                "resUsedTime": "161032",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "43000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "66862670",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "1",
                                "resCancelAmount": "43000",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240817",
                                "resUsedTime": "141832",
                                "resCardNo": "485479******7482",
                                "resCardNo1": "",
                                "resMemberStoreName": "의왕농협포일지점",
                                "resUsedAmount": "17100",
                                "resPaymentType": "3",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "72081997",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "120620350",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240816",
                                "resUsedTime": "113936",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주주식회사(온라인사업부)",
                                "resUsedAmount": "25400",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "59588457",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "129368424",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240815",
                                "resUsedTime": "064222",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "41700",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "48466482",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240814",
                                "resUsedTime": "180132",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주주식회사(온라인사업부)",
                                "resUsedAmount": "24400",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "45120043",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "172287656",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240808",
                                "resUsedTime": "154454",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "89140",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "59202449",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240807",
                                "resUsedTime": "085937",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "834600",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "44965925",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240803",
                                "resUsedTime": "214536",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주주식회사(온라인사업부)",
                                "resUsedAmount": "42000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "52688221",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "1",
                                "resCancelAmount": "42000",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "129368424",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240803",
                                "resUsedTime": "214322",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "39900",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "52675057",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240801",
                                "resUsedTime": "171733",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "의왕농협포일지점",
                                "resUsedAmount": "28900",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "66981646",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "120620350",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240723",
                                "resUsedTime": "164657",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "26000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "51133691",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240720",
                                "resUsedTime": "205524",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "19440",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "62645122",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240718",
                                "resUsedTime": "182810",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "19440",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "41303797",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240715",
                                "resUsedTime": "204138",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "26700",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "52732475",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240713",
                                "resUsedTime": "130155",
                                "resCardNo": "546111******0613",
                                "resCardNo1": "",
                                "resMemberStoreName": "천안농협하나로마트불당점",
                                "resUsedAmount": "28150",
                                "resPaymentType": "3",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "66293755",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "141447110",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240709",
                                "resUsedTime": "154721",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "26000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "66075881",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            },
                            {
                                "resUsedDate": "20240702",
                                "resUsedTime": "125758",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주주식회사(온라인사업부)",
                                "resUsedAmount": "46400",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "73517902",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "129368424",
                                "resCardName": "",
                                "commStartDate": "20240701",
                                "commEndDate": "20240930"
                            }
                        ],
                        [
                            {
                                "resUsedDate": "20241102",
                                "resUsedTime": "102351",
                                "resCardNo": "524140******7183",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주주식회사(온라인사업부)",
                                "resUsedAmount": "56000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "67204490",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "129368424",
                                "resCardName": "",
                                "commStartDate": "20241001",
                                "commEndDate": "20241103"
                            },
                            {
                                "resUsedDate": "20241102",
                                "resUsedTime": "100449",
                                "resCardNo": "524140******7183",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "67500",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "67008009",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20241001",
                                "commEndDate": "20241103"
                            },
                            {
                                "resUsedDate": "20241031",
                                "resUsedTime": "155009",
                                "resCardNo": "524140******7183",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주주식회사(온라인사업부)",
                                "resUsedAmount": "30000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "51489490",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "129368424",
                                "resCardName": "",
                                "commStartDate": "20241001",
                                "commEndDate": "20241103"
                            },
                            {
                                "resUsedDate": "20241018",
                                "resUsedTime": "121908",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "농협경제지주주식회사(온라인사업부)",
                                "resUsedAmount": "56000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "74491054",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "129368424",
                                "resCardName": "",
                                "commStartDate": "20241001",
                                "commEndDate": "20241103"
                            },
                            {
                                "resUsedDate": "20241010",
                                "resUsedTime": "163800",
                                "resCardNo": "546111******0613",
                                "resCardNo1": "",
                                "resMemberStoreName": "천안농협하나로마트불당점",
                                "resUsedAmount": "3800",
                                "resPaymentType": "3",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "75109109",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "141447110",
                                "resCardName": "",
                                "commStartDate": "20241001",
                                "commEndDate": "20241103"
                            },
                            {
                                "resUsedDate": "20241006",
                                "resUsedTime": "095009",
                                "resCardNo": "245",
                                "resCardNo1": "",
                                "resMemberStoreName": "이지웰주식회사",
                                "resUsedAmount": "9000",
                                "resPaymentType": "1",
                                "resInstallmentMonth": "",
                                "resApprovalNo": "70562343",
                                "resPaymentDueDate": "",
                                "resMemberStoreCorpNo": "",
                                "resMemberStoreType": "",
                                "resMemberStoreAddr": "",
                                "resMemberStoreTelNo": "",
                                "resAccountCurrency": "KRW",
                                "resHomeForeignType": "1",
                                "resCancelYN": "0",
                                "resCancelAmount": "",
                                "resVAT": "",
                                "resCashBack": "",
                                "resKRWAmt": "",
                                "resMemberStoreNo": "166456630",
                                "resCardName": "",
                                "commStartDate": "20241001",
                                "commEndDate": "20241103"
                            }
                        ]
                    ]
                ]

with open(result_filename, mode="w", encoding="utf8", newline='') as f:
    json.dump(parcedData_ALL,f, ensure_ascii=False, indent=4)
# ========== 카드 승인내역 받아오기 =============