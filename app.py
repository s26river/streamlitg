import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime,date,timedelta,timezone


def graph_plt():
    
    
    TITLE='日本のコロナ感染者数推移'

    st.title(f'{TITLE}')
   
    UNOW=datetime.now()
    JST=timezone(timedelta(hours=+9))
    NOW=UNOW+timedelta(hours=+9)
    TIME=datetime(NOW.year,NOW.month,NOW.day,NOW.hour,NOW.minute,tzinfo=JST)
    STIME=TIME.strftime("%Y年%m月%d日%H時%M分")
    st.write(f"感染者数推移{STIME}現在")
    df = pd.read_csv('https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv',parse_dates=True,index_col='Date')
    dfp=df
    dfp.columns.name="感染者数"
    dfp.index.name="日付"
    dfpc=dfp.rename(columns={'ALL':'全国','Aichi':'愛知県','Akita':'秋田県','Aomori':'青森県'\
,'Chiba':'千葉県','Ehime':'愛媛県','Fukui':'福井県','Fukuoka':'福岡県','Fukushima':'福島県'\
,'Gifu':'岐阜県','Gunma':'群馬県','Hiroshima':'広島県','Hokkaido':'北海道','Hyogo':'兵庫県'\
,'Ibaraki':'茨城県','Ishikawa':'石川県','Iwate':'岩手県','Kagawa':'香川県','Kagoshima':'鹿島県'\
,'Kanagawa':'神奈川県','Kochi':'高知県','Kumamoto':'熊本県','Kyoto':'京都府','Mie':'三重県','Miyagi':'宮城県'\
,'Miyazaki':'宮崎県','Nagano':'長野県','Nagasaki':'長崎県','Nara':'奈良県','Niigata':'新潟県','Oita':'大分県'\
,'Okayama':'岡山県','Okinawa':'沖縄県','Osaka':'大阪府','Saga':'佐賀県','Saitama':'埼玉県','Shiga':'滋賀県'\
,'Shimane':'島根県','Shizuoka':'静岡県','Tochigi':'栃木県','Tokushima':'徳島県','Tokyo':'東京都','Tottori':'鳥取県'\
,'Toyama':'富山県','Wakayama':'和歌山県','Yamagata':'山形県','Yamaguchi':'山口県','Yamanashi':'山梨県'})
    TITLE="コロナ新規陽性者数（県別）移動平均28日"
    dfpcd=dfpc[dfpc.index >= '2020-07-07']
    #dfpcd.to_excel(f'/content/drive/MyDrive/{TITLE}{STIME}.xlsx')
    dr=dfpcd.resample("7D").mean()
    dr07=dfpcd.rolling(window=7).mean()#移動平均7日
    dr28=dfpcd.rolling(window=28).mean()#移動平均28日
    chart_data = pd.DataFrame({"全国移動平均7日":dr07["全国"],"全国移動平均28日":dr28["全国"],
                               "東京都移動平均7日":dr07["東京都"],"東京都移動平均28日":dr28["東京都"],
                               "神奈川移動平均7日":dr07["神奈川県"],"神奈川移動平均28日":dr28["神奈川県"]})
    st.line_chart(chart_data)
    #st.table(chart_data)
    st.text('Version 1.9')
    # マークダウンテキスト
    #st.markdown('**Markdown is available **')

if __name__=='__main__':
    graph_plt()
