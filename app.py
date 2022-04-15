import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import numpy as np
import time
from datetime import datetime,date,timedelta,timezone
import pandas as pd
import numpy as np
import requests
import json
import plotly.express as px

st.write(f'<span style="color:maroon">日本酒ソムリエ</span>',unsafe_allow_html=True)

col1,col2= st.columns(2)

col1.image("sake1.jpg", use_column_width=True)
#col1.image("zakoshi.gif", use_column_width=True)
#col2.image("sake2.jpg", use_column_width=True)
#col3.image("sake3.jpg", use_column_width=True)

#エンドポイント
urls = {
"地域一覧": "https://muro.sakenowa.com/sakenowa-data/api/areas",
"銘柄一覧": "https://muro.sakenowa.com/sakenowa-data/api/brands",
"蔵元一覧": "https://muro.sakenowa.com/sakenowa-data/api/breweries",
"ランキング": "https://muro.sakenowa.com/sakenowa-data/api/rankings",
"フレーバーチャート": "https://muro.sakenowa.com/sakenowa-data/api/flavor-charts",
"フレーバータグ": "https://muro.sakenowa.com/sakenowa-data/api/flavor-tags",
"銘柄ごとフレーバータグ": "https://muro.sakenowa.com/sakenowa-data/api/brand-flavor-tags"}

#地域一覧(id,地域名)を取得する関数→戻り値json
@st.cache
def get_areas_response():
    areas_response = requests.get(urls.get("地域一覧")).json()
    return areas_response

#地域名を取得する関数→戻り値pandas
@st.cache
def get_df_areas_response():
    areas_response = get_areas_response()
    df_areas_response = pd.DataFrame(areas_response["areas"])
    return df_areas_response

#地域IDを取得する関数
@st.cache
def get_areaId(area):
  df_areas_response=get_df_areas_response()
  areaId = df_areas_response[df_areas_response['name'] == area]['id'].values
  return areaId

#蔵元名,ID一覧を取得→戻り値json
@st.cache
def get_breweries_response():
  breweries_response = requests.get(urls.get("蔵元一覧")).json()
  return breweries_response

#蔵元名,ID一覧をデータフレーム化 ※ＮＧ
@st.cache
def get_df_breweries():
  df_breweries = pd.DataFrame(get_breweries_response()['breweries'])
  return df_breweries

#選択した県の蔵元名　※ＮＧ
@st.cache
def get_df_breweries_ken(areaId):
  df_breweries = get_df_breweries()
  df_breweries_ken = df_breweries[df_breweries['areaId']==areaId]['name']
  return df_breweries_ken

# 蔵元IDを取得
@st.cache
def get_breweryId(select_breweries):
  df_breweries = get_df_breweries()
  breweryId = df_breweries[df_breweries['name']==select_breweries]['id']
  return breweryId

#銘柄名を取得
@st.cache
def get_brands_response():
  brands_response = requests.get(urls.get("銘柄一覧")).json()
  return brands_response

def sake(): 

    areas_response = get_areas_response()  #地域一覧(id,地域名)を取得
    df_areas_response=get_df_areas_response()
    areas = df_areas_response['name'].values  #地域名一覧
    select_areas = select_areas = st.sidebar.selectbox("好きな地域を選んでください", areas)
    areaId = get_areaId(select_areas) #地域IDを取得    
    breweries_response = get_breweries_response() #蔵元名一覧を取得
    #breweries = get_df_breweries_ken(areaId)
    breweries = [breweries["name"] for breweries in breweries_response["breweries"] if breweries["areaId"]==areaId]
    select_breweries = st.sidebar.selectbox("好きな蔵元を選んでください", breweries)
    # 蔵元IDを取得
    #breweryId = get_breweryId(select_breweries)
    breweryId = [breweries["id"] for breweries in breweries_response["breweries"] if breweries["name"]==select_breweries][0]
    
    # 銘柄名を取得
    #brands_response = requests.get(urls.get("銘柄一覧")).json()
    brands_response　get_brands_response()
    brands = [brands["name"] for brands in brands_response["brands"] if brands["breweryId"]==breweryId]
    select_brands = st.sidebar.selectbox("好きな銘柄を選んでください", brands)
    # 銘柄IDを取得
    brandId = [brands["id"] for brands in brands_response["brands"] if brands["name"]==select_brands][0]
    # フレーバーチャートを取得
    flavor_charts_response = requests.get(urls.get("フレーバーチャート")).json()
    flavor_charts = [flavor_charts for flavor_charts in flavor_charts_response["flavorCharts"] if flavor_charts["brandId"]==brandId]
    # plotlyでレーダーチャートを表示
    #st.markdown(f'## {select_brands}のフレーバーチャート')
    if st.checkbox(f'{select_brands}のフレーバーチャートを表示'):
        #st.write(f'<span style="color:green"> {select_brands}</span>のフレーバーチャート',unsafe_allow_html=True)
        try:
            df = pd.DataFrame(flavor_charts)
            df = df.drop('brandId', axis=1)
            # 見やすくするためにカラム名を変更、その後plotlyで読み込めるようにデータを転置
            df = df.rename(columns={'f1':'華やか', 'f2':'芳醇', 'f3':'重厚', 'f4':'穏やか', 'f5':'ドライ', 'f6':'軽快'}).T
            fig = px.line_polar(df, r=df[0], theta=df.index, line_close=True, range_r=[0,1],width=350,height=350)
            left_column,mid,right_column = st.columns(3)
            left_column.plotly_chart(fig)
            #right_column.plotly_chart(fig)
            #st.plotly_chart(fig)
            st.write(f'[さけのわAPI](https://sakenowa.com)のデータを表示しています')
            # フレーバーチャートのデータがないものもあるので例外処理
        except:
            #st.markdown('## この銘柄はフレーバーチャートを表示できません！！')
            st.write(f'<span style="color:red;background:pink">この銘柄はフレーバーチャートを表示できません！！</span>',unsafe_allow_html=True)
    
    #if st.button("ギャラリーの表示"):
    if st.checkbox('ギャラリーの表示'):
        stc.html(
            """
            <!DOCTYPE html>
            <html>
            <head><!-- 裏設定エリアの開始 -->
            <meta charset="utf-8"><!-- 文字化け防止 -->
            </head><!-- 裏設定エリアの終了 -->
            <body><!-- 画面に表示されるエリアの開始 -->
            わたしはもぐたんです。
            </body><!-- 画面に表示されるエリアの終了 -->
            </html>
            """)
        #stc.iframe("STREAMLITG.html",scrolling=True)
if __name__=='__main__':
    sake()
