import json
import requests
import streamlit as st
from PIL import Image
from PIL import ImageFont, ImageDraw, Image
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


st.set_page_config(
    page_title = "DEMEPRE",
    page_icon = "🌍",
    layout='wide'
)

zarathu_img = Image.open("C:/Users/김지희/pythonProject/image01.png")

col1,col2 = st.columns([1,1])

with col1 :
  # column 1 에 담을 내용
  st.title('')
with col2 :
  # column 2 에 담을 내용
  st.title('️')

# 컬럼2에 불러온 사진 표시하기
col1.image(zarathu_img, width=175)

st.markdown("<h1 style='color: #0090E3;'>️Demepre</h1>", unsafe_allow_html=True)
st.subheader("| Dementia Prediction")

st.subheader("")
st.subheader("")

url = requests.get(
    "https://lottie.host/45f57ea9-21b7-4440-9c81-e3d031c15f53/WKRlNi69x6.json")
url_json = dict()
if url.status_code == 200:
    url_json = url.json()
else:
    print("Error in URL")

st_lottie(url_json,
          # change the direction of our animation
          reverse=True,
          # height and width of animation
          height=600,
          width=600,
          # speed of animation
          speed=1,
          # means the animation will run forever like a gif, and not as a still image
          loop=True,
          # quality of elements used in the animation, other values are "low" and "medium"
          quality='high',
          # THis is just to uniquely identify the animation
          key='Family'
          )

st.subheader("")
st.subheader("")
st.subheader("")

# 텍스트를 중앙으로 정렬된 박스 내에 출력

st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center;">
        <p style="text-align: center; font-size: 24px; color: #0090E3;">
            <strong>치매를 밝게 비추는 AI 솔루션, DemePre</strong>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center;">
        <p style="text-align: center; font-size: 19px;">
            <strong>DemePre는 빅데이터 분석 및 AI 기술을 통해 치매 초기 징후를 감지하고</strong>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center;">
        <p style="text-align: center; font-size: 19px;">
            <strong>예방적 조치를 취해 조기 진단에 도움이 되는 솔루션을 도출하는 플랫폼입니다.</strong>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

url = requests.get(
    "https://lottie.host/494195b7-77aa-4056-b650-2777c4a5b5cd/9GldPwcdgV.json")
url_json = dict()
if url.status_code == 200:
    url_json = url.json()
else:
    print("Error in URL")

st.subheader("")
st.subheader("")
st.subheader("")
st.subheader("")
st.subheader("")
st.subheader("")

st_lottie(url_json,
          # change the direction of our animation
          reverse=True,
          # height and width of animation
          height=600,
          width=600,
          # speed of animation
          speed=1,
          # means the animation will run forever like a gif, and not as a still image
          loop=True,
          # quality of elements used in the animation, other values are "low" and "medium"
          quality='high'
          )

st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center;">
        <p style="text-align: center; font-size: 24px; color: #0090E3;">
            <strong>더 나은 삶, 미래로 향하는 길</strong>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center;">
        <p style="text-align: center; font-size: 19px;">
            <strong>
                Demepre는 환자와 가족들에게 더 나은 삶의 질을 제공하여
            </strong>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center;">
        <p style="text-align: center; font-size: 19px;">
            <strong>
                보다 건강한 미래를 향해 함께 나아가고자 합니다.
            </strong>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)