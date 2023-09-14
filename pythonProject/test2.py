###### 환자 이메일 : nia+279@rowan.kr
###### terminal에 입력 -> streamlit run test2.py
!pip install streamlit_option_menu
!pip install --upgrade pip

import streamlit as st
from datetime import datetime, timedelta, date
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
from sklearn.model_selection import train_test_split

st.set_page_config(
    page_title = "Analysis",
    page_icon = "📊",
    layout='wide'
)

st.title('DemePre')
st.subheader('치매 고위험군 웨어러블 라이프로그 분석')
st.title('')

# 이메일 입력 위젯 생성
desired_email = st.text_input("이메일 입력", "")

#################### 수면 데이터 ####################

df2 = pd.read_csv("C:/Users/김지희/Desktop/09.06/TRACK 02/128.치매 고위험군 라이프로그/01.데이터/1.Training/원천데이터/2.수면/train_sleep.csv")

# 입력된 이메일 주소를 가진 환자만 선택
filtered_df2 = df2[df2['EMAIL'] == desired_email]

# 필요한 열만 선택
filtered_df2 = filtered_df2[['sleep_bedtime_start', 'sleep_bedtime_end', 'sleep_hr_average', 'sleep_duration', 'sleep_score_deep', 'sleep_score_rem', 'sleep_score_efficiency', 'sleep_restless']]

# "activity_day_start"와 "activity_day_end" 열을 datetime 형식으로 변환 (타임존 정보 제거)
filtered_df2['sleep_bedtime_start'] = pd.to_datetime(filtered_df2['sleep_bedtime_start']).dt.tz_localize(None)
filtered_df2['sleep_bedtime_end'] = pd.to_datetime(filtered_df2['sleep_bedtime_end']).dt.tz_localize(None)

# 사용자가 선택할 수 있는 기간 목록 생성
available_periods = []
current_date = filtered_df2['sleep_bedtime_start'].min()

while current_date <= filtered_df2['sleep_bedtime_end'].max():
    end_of_week = min(current_date + timedelta(days=6), filtered_df2['sleep_bedtime_end'].max())
    period_str = f"{current_date.strftime('%Y-%m-%d')} ~ {end_of_week.strftime('%Y-%m-%d')}"
    available_periods.append(period_str)
    current_date += timedelta(days=7)

selected_period = st.selectbox("주간 기간 선택", available_periods)

# 사용자가 주간 기간을 선택하지 않은 경우를 처리
if selected_period is not None:
    # 주간 기간 선택 문자열에서 시작 날짜와 끝 날짜 추출
    start_date_str, end_date_str = selected_period.split(' ~ ')
    start_date_str = start_date_str.strip()
    end_date_str = end_date_str.strip()

    # 시작 날짜와 끝 날짜를 datetime 형식으로 변환
    start_date = pd.to_datetime(start_date_str)
    end_date = pd.to_datetime(end_date_str)

    # 선택한 주간 기간에 해당하는 데이터 필터링
    filtered_period_df2 = filtered_df2[
        (filtered_df2['sleep_bedtime_start'] >= start_date) &
        (filtered_df2['sleep_bedtime_end'] <= end_date)
        ]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader('평균 심박수')

        average_hr = filtered_period_df2['sleep_hr_average'].mean()

        # 결과 출력
        st.markdown(
            f"<br><br><div style='text-align: center;'><span style='font-size:48px; font-weight:bold;'> ❤️{average_hr:.0f} BPM</span></div>",
            unsafe_allow_html=True
        )
    with col2:
        st.subheader('수면 시간')
        average_sleep_score = filtered_period_df2['sleep_duration'].mean()
        average_sleep_hours = average_sleep_score / 3600
        st.markdown(
            f"<br><br><div style='text-align: center;'><span style='font-size:38px; font-weight:bold;'>평균 {average_sleep_hours:.0f}시간</span></div>",
            unsafe_allow_html=True
        )
    with col3:
        st.subheader('수면 그래프')
        average_deep_score = filtered_period_df2['sleep_score_deep'].mean()
        average_efficiency_score = filtered_period_df2['sleep_score_efficiency'].mean()
        average_rem_score = filtered_period_df2['sleep_score_rem'].mean()

        # 평균 값을 파이 차트로 시각화
        fig = px.pie(
            values=[average_deep_score, average_efficiency_score, average_rem_score],
            names=['깊은 수면 점수', '수면 효율 점수', '램수면 점수'],
            title='주간 수면 점수 평균',
        )

        # 파이 차트 크기 조절
        fig.update_layout(
            autosize=False,
            width=350,  # 원하는 너비로 조절
            height=400,  # 원하는 높이로 조절
        )

        # 데이터 값 텍스트 크기 조절
        fig.update_traces(textinfo='percent', textfont_size=20)

        # 범례 위치 설정
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="right"))

        # 결과 출력
        st.plotly_chart(fig)

    with col4:
        st.subheader('뒤척임 비율')
        average_restless = filtered_period_df2['sleep_restless'].mean()
        st.markdown(
            f"<br><br><div style='text-align: center;'><span style='font-size:48px; font-weight:bold;'>{average_restless:.0f}%</span></div>",
            unsafe_allow_html=True
        )

else:
    st.warning("주간 기간을 선택하세요.")

#################### 걸음걸이 데이터 ####################

df = pd.read_csv("C:/Users/김지희/Desktop/09.06/TRACK 02/128.치매 고위험군 라이프로그/01.데이터/1.Training/원천데이터/1.걸음걸이/train_activity.csv")

# 입력된 이메일 주소를 가진 환자만 선택
filtered_df = df[df['EMAIL'] == desired_email]

# "activity_day_start"와 "activity_day_end" 열을 datetime 형식으로 변환 (타임존 정보 제거)
filtered_df['activity_day_start'] = pd.to_datetime(filtered_df['activity_day_start']).dt.tz_localize(None)
filtered_df['activity_day_end'] = pd.to_datetime(filtered_df['activity_day_end']).dt.tz_localize(None)

# 사용자가 선택할 수 있는 기간 목록 생성
available_periods = []
current_date = filtered_df['activity_day_start'].min()

while current_date <= filtered_df['activity_day_end'].max():
    end_of_week = min(current_date + timedelta(days=6), filtered_df['activity_day_end'].max())
    period_str = f"{current_date.strftime('%Y-%m-%d')} ~ {end_of_week.strftime('%Y-%m-%d')}"
    available_periods.append(period_str)
    current_date += timedelta(days=7)

# 사용자가 주간 기간을 선택하지 않은 경우를 처리
if selected_period is not None:
    # 주간 기간 선택 문자열에서 시작 날짜와 끝 날짜 추출
    start_date_str, end_date_str = selected_period.split(' ~ ')
    start_date_str = start_date_str.strip()
    end_date_str = end_date_str.strip()

    # 시작 날짜와 끝 날짜를 datetime 형식으로 변환
    start_date = pd.to_datetime(start_date_str)
    end_date = pd.to_datetime(end_date_str)

    # 선택한 주간 기간에 해당하는 데이터 필터링
    filtered_period_df = filtered_df[
        (filtered_df['activity_day_start'] >= start_date) &
        (filtered_df['activity_day_end'] <= end_date)
        ]

    # 주간 강도별 활동 시간 데이터 선택
    chart_data_activity = filtered_period_df[['activity_day_start', 'activity_high', 'activity_medium', 'activity_low']]
    chart_data_activity['activity_day_start'] = chart_data_activity['activity_day_start'].dt.strftime('%Y-%m-%d')
    chart_data_activity.set_index('activity_day_start', inplace=True)

    # 원하는 색상 리스트 생성
    color_range = ['#00598C', '#0090E3', '#77C5FF']

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader('강도별 활동 시간')
        st.bar_chart(chart_data_activity[['activity_high', 'activity_medium', 'activity_low']],
                     use_container_width=True,
                     color=color_range)
        # 합계 데이터 표시
        st.markdown(
            f"<div style='text-align: center;'><span style='font-size:20px; font-weight:bold;'>고강도 활동 시간 {chart_data_activity['activity_high'].sum()}분</span></div>",
            unsafe_allow_html=True)
        st.markdown(
            f"<div style='text-align: center;'><span style='font-size:20px; font-weight:bold;'>중강도 활동 시간 {chart_data_activity['activity_medium'].sum()}분</span></div>",
            unsafe_allow_html=True)
        st.markdown(
            f"<div style='text-align: center;'><span style='font-size:20px; font-weight:bold;'>저강도 활동 시간 {chart_data_activity['activity_low'].sum()}분</span></div>",
            unsafe_allow_html=True)

    # 주간 걸음 수 그래프 출력
    with col2:
        st.subheader('걸음 수')
        # 이전 주간 데이터 가져오기
        end_of_previous_week = start_date - timedelta(days=1)
        start_of_previous_week = end_of_previous_week - timedelta(days=6)
        previous_period_str = f"{start_of_previous_week.strftime('%Y-%m-%d')} ~ {end_of_previous_week.strftime('%Y-%m-%d')}"
        previous_data = filtered_df[
            (filtered_df['activity_day_start'] >= start_of_previous_week) &
            (filtered_df['activity_day_start'] <= end_of_previous_week)
            ]

        # 주간 기간을 "2020-10-24 ~ 2020-10-30"과 같이 나타내기
        week_period = f"{start_date_str} ~ {end_date_str}"

        # 주간 걸음 수 데이터 선택
        chart_data_movement = pd.DataFrame({'주간 기간': [week_period, previous_period_str],
                                            '주간 걸음 수': [filtered_period_df['activity_steps'].sum(),
                                                        previous_data['activity_steps'].sum()]})
        # 걸음 수 감소량 계산
        distance_reduction = filtered_period_df['activity_steps'].sum() - previous_data[
            'activity_steps'].sum()

        # 바 그래프 색상 설정
        chart_movement = alt.Chart(chart_data_movement).mark_bar().encode(
            x=alt.X('주간 기간:N', title=''),
            y=alt.Y('주간 걸음 수:Q', title=''),
            color=alt.Color('주간 기간:N', title='기간',
                            scale=alt.Scale(domain=[week_period, previous_period_str], range=['#0090E3', '#00598C']))
        ).properties(width=420, height=400)

        # 걸음 수 변화에 따라 메시지 생성
        if distance_reduction > 0:
            change_message = f"<span style='font-size:20px; font-weight:bold;'> 지난 주보다 걸음 수가 {distance_reduction}걸음 늘었어요 </span>"
        else:
            change_message = f"<span style='font-size:20px; font-weight:bold;'> 지난 주보다 걸음 수가 {abs(distance_reduction)}걸음 줄었어요 </span>"

        # 범례 위치 조정
        chart_movement = chart_movement.configure_legend(orient='bottom')
        st.altair_chart(chart_movement)

        st.markdown(f"<p style='text-align: center;'>{change_message}</p>", unsafe_allow_html=True)

    with col3:
        st.subheader('활동 점수')

        # 선택된 주간 기간의 활동 점수 평균 계산
        average_activity_score = filtered_period_df['activity_score'].mean()

        # 목표 활동 점수 가져오기
        daily_target_score = filtered_period_df['activity_score_meet_daily_targets'].iloc[0]

        # 점수 비교 및 메시지 생성
        if average_activity_score >= daily_target_score:
            result_message = f"<br><br><span style='font-size:38px; font-weight:bold;'> {average_activity_score:.0f}점 </span> <span style='font-size:28px; font-weight:bold;'><br>목표 달성🎉 </span>"
        else:
            result_message = f"<br><br><span style='font-size:38px; font-weight:bold;'> {average_activity_score:.0f}점 </span> <span style='font-size:28px; font-weight:bold;'><br>목표 달성 실패😔 </span>"

        st.markdown(f"<p style='text-align: center;'>{result_message}</p>", unsafe_allow_html=True)

    with col4:
        st.subheader('치매 발병 확률')
        # weekly_predictions.csv 파일 경로 설정
        csv_file_path = "C:/Users/김지희/Desktop/GWAICHALLENGE/TRACK02/weekly_predictions.csv"

        # weekly_predictions.csv 파일 읽기
        weekly_predictions_df = pd.read_csv(csv_file_path)

        # 주간 기간 선택 문자열에서 시작 날짜와 끝 날짜 추출
        start_date_str, end_date_str = selected_period.split(' ~ ')
        start_date_str = start_date_str.strip()
        end_date_str = end_date_str.strip()

        # 시작 날짜와 끝 날짜를 datetime 형식으로 변환
        start_date = pd.to_datetime(start_date_str)
        end_date = pd.to_datetime(end_date_str)

        # 주간 기간이 weekly_range에 속하는지 확인
        is_within_range = weekly_predictions_df['weekly_range'].apply(
            lambda x: start_date <= pd.to_datetime(x.split(' ~ ')[0]) <= end_date)

        # 속하는 주간의 Dementia_Probability 가져오기
        if any(is_within_range):
            dementia_probability = weekly_predictions_df[is_within_range]['Dementia_Probability'].values[0]
            # Dementia_Probability 값을 퍼센트로 변환하고 소수점 3자리까지 표시
            dementia_probability_percent = dementia_probability * 100
            formatted_dementia_probability = "{:.0f}%".format(dementia_probability_percent)

            col4.markdown(
                f"<br><br><div style='text-align: center;'><span style='font-size:75px; font-weight:bold; color:red;'>{formatted_dementia_probability}</span></div>",
                unsafe_allow_html=True
            )

        else:
            col4.warning("선택한 주간 기간에 대한 데이터가 없습니다.")

else:
    st.warning("주간 기간을 선택하세요.")
