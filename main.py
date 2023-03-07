import pandas as pd
import streamlit as st
import io
import pickle
import numpy as np
import scikit-learn
from scikit-learn.preprocessing import RobustScaler

#настраиваем вид страницы streamlit
st.set_page_config(page_title='Sergey Kuznetsov, Ya Practicum project for Kaggle competition',
                   layout='wide',
                   initial_sidebar_state='expanded')

st.title('Введение в проект', anchor='intro')
st.sidebar.header('[Введение в проект](#intro)')

#input
st.header('Проверим ваше сердце', anchor='heart')
st.sidebar.header('[Проверим ваше сердце](#heart)')
st.subheader('Заполните информацию о своём здоровье на данный момент, чтобы узнать, какой у вас риск сердечного приступа.')
lc, rc = st.columns(2)
ap_hi = lc.slider('Систолическое (верхнее) давление', 80, 150 )
ap_lo = rc.slider('Диастолическое (нижнее) давление', 40, 100 )

lc.checkbox("Курю", key="smoke")
rc.selectbox("Уровень холестерина",['Низкий', 'Средний', 'Высокий'], key="cholesterol")
rc.write('')
lc.write('')
st.write('')


#output
with lc:
    st.header('Результаты')
    st.write('Давление:', ap_hi,'/',ap_lo)
    if st.session_state.smoke == False:
        st.write('Не курит')
    else:
        st.write('Курит')

with rc:
    st.write('')
    st.write('')
    st.write('Уровень холестерина:', st.session_state.cholesterol.lower())


def load():
    with open('model_RFC.pcl', 'rb') as mod:
        return pickle.load(mod)
model_test = load()

#try:
#    model_test = load()
#    st.write('Модель загружена')
#except:
#    st.write('Модель НЕ загружена')

age = 65*365
height = 168
weight = 110
ap_hi = 150
ap_lo = 90
gender = 1
cholesterol = 1
gluc = 1
smoke = 1
alco = 1
active = 0

#data = [[age,height,weight,ap_hi,ap_lo,gender,cholesterol,gluc,smoke,alco,active ]]

data = pd.DataFrame({'age': age,
              'height': height,
              'weight': weight,
              'ap_hi': ap_hi,
              'ap_lo': ap_lo,
              'gender_0': gender,
              'gender_1': 0,
              'cholesterol_0': cholesterol,
              'cholesterol_1': 0,
              'cholesterol_2': 0,
              'gluc_0': gluc,
              'gluc_1': 0,
              'gluc_2': 0,
              'smoke_0': 0,
              'smoke_1': smoke,
              'alco_0': 0,
              'alco_1': alco,
              'active_0': active,
              'active_1': 0
              }, index=[0])
st.write(data.head())

numeric = ['age', 'ap_hi', 'ap_lo', 'height', 'weight']

features = pd.read_csv('features.csv')

scaler = RobustScaler()
scaler.fit(features[numeric])
data[numeric] = scaler.transform(data[numeric])



st.write(data.head())

pr = model_test.predict_proba(data)[:,1]



st.write('Вероятность риска развития сердечно-сосудистого заболевания составляет {}'.format(pr))
st.write('Другие проекты в [моём профиле на GitHub](https://github.com/Kuuuzya)')