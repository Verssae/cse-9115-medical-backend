import requests
import json

URL='http://127.0.0.1:5000/post'
data = {
  "details": [
    "왼쪽 팔꿈치",
    "꼬리뼈"
  ],
  "diagnosis": "수술",
  "diagnosisDuration": "1달 이내",
  "duration": 3,
  "elbowFunction": [
    "씻기",
    "식사"
  ],
  "home": True,
  "medicine": "아니요",
  "motion": 60,
  "overviews": [
    "오른쪽 팔"
  ],
  "pain": [1, 2],
  "stability": 0
}

data2 = {
  "details": [
    "왼쪽 팔꿈치",
    "꼬리뼈"
  ],
  "diagnosis": "수술",
  "diagnosisDuration": "1달 이내",
  "duration": 3,
  "elbowFunction": [],
  "home": False,
  "medicine": "아니요",
  "motion": 60,
  "overviews": [
    "왼쪽 다리"
  ],
  "pain": 1,
  "stability": 10
}


# res = requests.post(URL, data=json.dumps(data))
res2 = requests.post(URL, data=json.dumps(data2))
# print(res)
print(res2)
print(res2.content)
