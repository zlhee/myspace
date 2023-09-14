# terminal에 입력 -> streamlit run RESULT.py
import streamlit as st
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import altair as alt
import plotly.express as px

######################## 라이프로그 분석 페이지 ########################

st.set_page_config(
    page_title = "Analysis",
    page_icon = "📊",
    layout='wide'
)

st.title('김강원님 라이프로그 분석 결과')

# 이메일 입력 위젯 생성
desired_email = st.sidebar.text_input("환자 이메일 입력", "")

# 날짜 범위 입력 위젯 생성
start_date = st.sidebar.date_input("시작 날짜", datetime(2020, 1, 1))
end_date = st.sidebar.date_input("끝 날짜", datetime(2021, 12, 31))

# 탭 생성
tab1, tab2 = st.tabs(['걸음걸이', '수면'])

with tab1:
     # tab A 를 누르면 표시될 내용
     st.subheader('주간 강도별 활동 시간')
     df2 = pd.read_csv("C:/Users/김지희/Desktop/09.06/TRACK 02/128.치매 고위험군 라이프로그/01.데이터/1.Training/원천데이터/1.걸음걸이/train_activity.csv")

     # 입력된 이메일 주소를 가진 환자만 선택
     filtered_df = df2[df2['EMAIL'] == desired_email]

     # 필요한 열만 선택
     filtered_df = filtered_df[
         ['activity_day_start', 'activity_day_end', 'activity_high', 'activity_medium', 'activity_low']]

     # "activity_day_start"와 "activity_day_end" 열을 datetime 형식으로 변환 (타임존 정보 제거)
     filtered_df['activity_day_start'] = pd.to_datetime(filtered_df['activity_day_start']).dt.tz_localize(None)
     filtered_df['activity_day_end'] = pd.to_datetime(filtered_df['activity_day_end']).dt.tz_localize(None)

     # 사용자가 선택할 수 있는 기간 목록 생성
     available_periods = []
     current_date = filtered_df['activity_day_start'].min()
     while current_date <= filtered_df['activity_day_start'].max():
         end_of_week = min(current_date + timedelta(days=6), filtered_df['activity_day_start'].max())
         period_str = f"{current_date.strftime('%Y-%m-%d')} ~ {end_of_week.strftime('%Y-%m-%d')}"
         available_periods.append(period_str)
         current_date += timedelta(days=7)
     # 선택한 주간 기간에 해당하는 데이터 필터링
     selected_period = st.sidebar.selectbox("주간 기간 선택", available_periods)

     # 선택된 기간이 없는 경우 처리
     if selected_period:
         # 선택한 주간 기간의 시작과 끝 날짜 가져오기
         start_date_str, end_date_str = selected_period.split(" ~ ")
         start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
         end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

         selected_df = filtered_df[
             (filtered_df['activity_day_start'] >= start_date) &
             (filtered_df['activity_day_start'] <= end_date)
             ]

         # 바 그래프 그리기 (날짜 중 'day'만을 x 축으로 사용)
         chart_data = selected_df[['activity_day_start', 'activity_high', 'activity_medium', 'activity_low']]
         chart_data['activity_day_start'] = chart_data['activity_day_start'].dt.day
         chart_data.set_index('activity_day_start', inplace=True)

         # 원하는 색상 리스트 생성
         color_range = ['#00598C', '#0090E3', '#77C5FF']

         st.bar_chart(chart_data, use_container_width=True, color=color_range)
     else:
         st.warning("주간 기간을 선택해주세요.")

     st.title("")
     st.title("")
     st.title("")
     st.title("")
     st.title("")

     st.subheader('주간 이동거리') # 지난주 이동거리 데이터와 같이 보여줄 것
     # activity_daily_movement
     df2 = pd.read_csv("C:/Users/김지희/Desktop/09.06/TRACK 02/128.치매 고위험군 라이프로그/01.데이터/1.Training/원천데이터/1.걸음걸이/train_activity.csv")

     # 입력된 이메일 주소를 가진 환자만 선택
     patient_data = df2[df2['EMAIL'] == desired_email]

     # 필요한 열만 선택
     patient_data = patient_data[['EMAIL', 'activity_day_start', 'activity_day_end', 'activity_daily_movement']]

     # "activity_day_start"와 "activity_day_end" 열을 datetime 형식으로 변환 (타임존 정보 제거)
     patient_data['activity_day_start'] = pd.to_datetime(patient_data['activity_day_start']).dt.tz_localize(None)
     patient_data['activity_day_end'] = pd.to_datetime(patient_data['activity_day_end']).dt.tz_localize(None)

     # 선택된 기간이 없는 경우 처리
     if selected_period:
         # 선택한 주간 기간의 시작과 끝 날짜 가져오기
         start_date_str, end_date_str = selected_period.split(" ~ ")
         start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
         end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

         selected_data = patient_data[
             (patient_data['activity_day_start'] >= start_date) &
             (patient_data['activity_day_start'] <= end_date)
             ]

         # 주간 기간을 "2020-10-24 ~ 2020-10-30"과 같이 나타내기
         week_period = f"{start_date_str} ~ {end_date_str}"

         # 이전 주간 데이터 가져오기
         end_of_previous_week = start_date - timedelta(days=1)
         start_of_previous_week = end_of_previous_week - timedelta(days=6)
         previous_period_str = f"{start_of_previous_week.strftime('%Y-%m-%d')} ~ {end_of_previous_week.strftime('%Y-%m-%d')}"
         previous_data = patient_data[
             (patient_data['activity_day_start'] >= start_of_previous_week) &
             (patient_data['activity_day_start'] <= end_of_previous_week)
             ]

         # 바 그래프 그리기 (주간 기간과 주간 이동 거리 비교)
         chart_data = pd.DataFrame({'주간 기간': [week_period, previous_period_str],
                                    '주간 이동 거리': [selected_data['activity_daily_movement'].sum(),
                                                 previous_data['activity_daily_movement'].sum()]})

         # 바 그래프 색상 설정
         chart = alt.Chart(chart_data).mark_bar().encode(
             x=alt.X('주간 기간:N', title='기간(지난 주 / 이번 주)'),
             y=alt.Y('주간 이동 거리:Q', title='이동거리', axis=alt.Axis(format='~s')),
             color=alt.Color('주간 기간:N', title='기간',
                             scale=alt.Scale(domain=[week_period, previous_period_str], range=['#0090E3', '#00598C']))
         ).properties(width=900, height=400)

         st.altair_chart(chart)

     else:
         st.warning("주간 기간을 선택해주세요.")

     st.title("")
     st.title("")
     st.title("")
     st.title("")
     st.title("")

     st.subheader('주간 걸음 수') # 지난주 걸음 수 데이터와 같이 보여줄 것
     # activity_steps
     df2 = pd.read_csv(
         "C:/Users/김지희/Desktop/09.06/TRACK 02/128.치매 고위험군 라이프로그/01.데이터/1.Training/원천데이터/1.걸음걸이/train_activity.csv")

     # 입력된 이메일 주소를 가진 환자만 선택
     patient_data2 = df2[df2['EMAIL'] == desired_email]

     # 필요한 열만 선택
     patient_data2 = patient_data2[['EMAIL', 'activity_day_start', 'activity_day_end', 'activity_steps']]

     # "activity_day_start"와 "activity_day_end" 열을 datetime 형식으로 변환 (타임존 정보 제거)
     patient_data2['activity_day_start'] = pd.to_datetime(patient_data2['activity_day_start']).dt.tz_localize(None)
     patient_data2['activity_day_end'] = pd.to_datetime(patient_data2['activity_day_end']).dt.tz_localize(None)

     # 선택된 기간이 없는 경우 처리
     if selected_period:
         # 선택한 주간 기간의 시작과 끝 날짜 가져오기
         start_date_str, end_date_str = selected_period.split(" ~ ")
         start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
         end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

         selected_data = patient_data2[
             (patient_data2['activity_day_start'] >= start_date) &
             (patient_data2['activity_day_start'] <= end_date)
             ]

         # 주간 기간을 "2020-10-24 ~ 2020-10-30"과 같이 나타내기
         week_period = f"{start_date_str} ~ {end_date_str}"

         # 이전 주간 데이터 가져오기
         end_of_previous_week = start_date - timedelta(days=1)
         start_of_previous_week = end_of_previous_week - timedelta(days=6)
         previous_period_str = f"{start_of_previous_week.strftime('%Y-%m-%d')} ~ {end_of_previous_week.strftime('%Y-%m-%d')}"
         previous_data = patient_data2[
             (patient_data2['activity_day_start'] >= start_of_previous_week) &
             (patient_data2['activity_day_start'] <= end_of_previous_week)
             ]

         # 바 그래프 그리기 (주간 기간과 주간 이동 거리 비교)
         chart_data = pd.DataFrame({'주간 기간': [week_period, previous_period_str],
                                    '주간 걸음 수': [selected_data['activity_steps'].sum(),
                                                 previous_data['activity_steps'].sum()]})

         # 바 그래프 색상 설정
         chart = alt.Chart(chart_data).mark_bar().encode(
             x=alt.X('주간 기간:N', title='기간(지난 주 / 이번 주)'),
             y=alt.Y('주간 걸음 수:Q', title='걸음 수', axis=alt.Axis(format='~s')),
             color=alt.Color('주간 기간:N', title='기간',
                             scale=alt.Scale(domain=[week_period, previous_period_str], range=['#0090E3', '#00598C']))
         ).properties(width=900, height=400)

         st.altair_chart(chart)

     else:
         st.warning("주간 기간을 선택해주세요.")


with st.sidebar:
    choice = option_menu("", ["라이프로그 분석", "치매 예측"],
                         icons=['bi bi-bar-chart-line', 'bi bi-graph-up-arrow'],
                         styles={
        "container": {"padding": "4!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#0090E3"},
    }
    )

with tab2:
     # tab B 를 누르면 표시될 내용
     st.subheader('주간 수면 점수')

     # 데이터 파일 경로 변경
     df3 = pd.read_csv("C:/Users/김지희/Desktop/09.06/TRACK 02/128.치매 고위험군 라이프로그/01.데이터/1.Training/원천데이터/2.수면/train_sleep.csv")

     # 입력된 이메일 주소를 가진 환자만 선택
     patient_data = df3[df3['EMAIL'] == desired_email]

     # 필요한 열만 선택
     patient_data = patient_data[
         ['EMAIL', 'sleep_bedtime_start', 'sleep_bedtime_end', 'sleep_score_deep', 'sleep_score_disturbances',
          'sleep_score_efficiency']]

     # "sleep_bedtime_start"와 "sleep_bedtime_end" 열을 datetime 형식으로 변환 (타임존 정보 제거)
     patient_data['sleep_bedtime_start'] = pd.to_datetime(patient_data['sleep_bedtime_start']).dt.tz_localize(None)
     patient_data['sleep_bedtime_end'] = pd.to_datetime(patient_data['sleep_bedtime_end']).dt.tz_localize(None)

     # 사용자가 선택할 수 있는 기간 목록 생성
     available_periods = []
     current_date = patient_data['sleep_bedtime_start'].min()
     while current_date <= patient_data['sleep_bedtime_start'].max():
         end_of_week = min(current_date + timedelta(days=6), patient_data['sleep_bedtime_start'].max())
         period_str = f"{current_date.strftime('%Y-%m-%d')} ~ {end_of_week.strftime('%Y-%m-%d')}"
         available_periods.append(period_str)
         current_date += timedelta(days=7)

     # 선택된 기간이 없는 경우 처리
     if selected_period:
         # 선택한 주간 기간의 시작과 끝 날짜 가져오기
         start_date_str, end_date_str = selected_period.split(" ~ ")
         start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
         end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

         selected_data = patient_data[
             (patient_data['sleep_bedtime_start'] >= start_date) &
             (patient_data['sleep_bedtime_start'] <= end_date)
             ]

         # x축 index에 "day"만 나타내기 위해 'sleep_bedtime_start' 열에서 'day' 정보 추출
         selected_data['day'] = selected_data['sleep_bedtime_start'].dt.day

         # "sleep_score_deep", "sleep_score_disturbances", "sleep_score_efficiency"의 주간 평균 계산
         selected_data = selected_data.groupby('day')[
             ['sleep_score_deep', 'sleep_score_disturbances', 'sleep_score_efficiency']].mean().reset_index()

         # Line 그래프 그리기 (세 개의 변수를 하나의 그래프로 나타내기)
         chart_data = pd.melt(selected_data, id_vars=['day'],
                              value_vars=['sleep_score_deep', 'sleep_score_disturbances', 'sleep_score_efficiency'])

         chart = alt.Chart(chart_data).mark_line().encode(
             x=alt.X('day:O', title='일', axis=alt.Axis(labelAngle=0)),
             y=alt.Y('value:Q', title='수면 점수'),
             color=alt.Color('variable:N', title='수면 변수',
                             scale=alt.Scale(
                                 domain=['sleep_score_deep', 'sleep_score_disturbances', 'sleep_score_efficiency'],
                                 range=['#0090E3', 'red', '#00598C']))
         ).properties(width=900, height=300)

         st.altair_chart(chart)

     else:
         st.warning("주간 기간을 선택해주세요.")

     st.title("")
     st.title("")
     st.title("")
     st.title("")
     st.title("")

     st.subheader('주간 수면 종합 점수')
     # 데이터 파일 경로 변경
     df3 = pd.read_csv(
         "C:/Users/김지희/Desktop/09.06/TRACK 02/128.치매 고위험군 라이프로그/01.데이터/1.Training/원천데이터/2.수면/train_sleep.csv")

     # 입력된 이메일 주소를 가진 환자만 선택
     patient_data = df3[df3['EMAIL'] == desired_email]

     # 필요한 열만 선택
     patient_data = patient_data[['EMAIL', 'sleep_bedtime_start', 'sleep_bedtime_end', 'sleep_score']]

     # "sleep_bedtime_start"와 "sleep_bedtime_end" 열을 datetime 형식으로 변환 (타임존 정보 제거)
     patient_data['sleep_bedtime_start'] = pd.to_datetime(patient_data['sleep_bedtime_start']).dt.tz_localize(None)
     patient_data['sleep_bedtime_end'] = pd.to_datetime(patient_data['sleep_bedtime_end']).dt.tz_localize(None)

     # 사용자가 선택할 수 있는 기간 목록 생성
     available_periods = []
     current_date = patient_data['sleep_bedtime_start'].min()
     while current_date <= patient_data['sleep_bedtime_start'].max():
         end_of_week = min(current_date + timedelta(days=6), patient_data['sleep_bedtime_start'].max())
         period_str = f"{current_date.strftime('%Y-%m-%d')} ~ {end_of_week.strftime('%Y-%m-%d')}"
         available_periods.append(period_str)
         current_date += timedelta(days=7)

     # 선택된 기간이 없는 경우 처리
     if selected_period:
         # 선택한 주간 기간의 시작과 끝 날짜 가져오기
         start_date_str, end_date_str = selected_period.split(" ~ ")
         start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
         end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

         selected_data = patient_data[
             (patient_data['sleep_bedtime_start'] >= start_date) &
             (patient_data['sleep_bedtime_start'] <= end_date)
             ]

         # "sleep_score"의 주간 평균 계산
         avg_sleep_score = selected_data['sleep_score'].mean()

         # 결과 출력
         st.write(f"<span style='font-size: 30px; font-weight: bold; color: #0090E3;'>평균  {avg_sleep_score:.2f}</span>",
                  unsafe_allow_html=True)

     else:
         st.warning("주간 기간을 선택해주세요.")