import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime,date,timedelta,timezone
import pandas as pd
import numpy as np
import requests
import json
import plotly.express as px

"""
### 日本酒ソムリエ
#### [さけのわAPI](https://sakenowa.com)のデータを表示しています 
"""
def sake(): 
    
    # エンドポイント
    urls = {
    "地域一覧": "https://muro.sakenowa.com/sakenowa-data/api/areas",
    "銘柄一覧": "https://muro.sakenowa.com/sakenowa-data/api/brands",
    "蔵元一覧": "https://muro.sakenowa.com/sakenowa-data/api/breweries",
    "ランキング": "https://muro.sakenowa.com/sakenowa-data/api/rankings",
    "フレーバーチャート": "https://muro.sakenowa.com/sakenowa-data/api/flavor-charts",
    "フレーバータグ": "https://muro.sakenowa.com/sakenowa-data/api/flavor-tags",
    "銘柄ごとフレーバータグ": "https://muro.sakenowa.com/sakenowa-data/api/brand-flavor-tags",
    }
        # 地域名を取得
    #areas_response = requests.get(urls.get("地域一覧")).json()
    #areas = [area["name"] for area in areas_response["areas"]]
    #リスト内包表記をPANDASに変更
    areas_response = requests.get("https://muro.sakenowa.com/sakenowa-data/api/areas").json()['areas']
    df=pd.DataFrame(areas_response).set_index('id')
    areas=df['name']
    select_areas = st.sidebar.selectbox("好きな地域を選んでください", areas)
    # 地域IDを取得
    #areaId = [area["id"] for area in areas_response["areas"] if area["name"]==select_areas][0]
    areaId = df['id']
    # 蔵元名を取得
    breweries_response = requests.get(urls.get("蔵元一覧")).json()
    breweries = [breweries["name"] for breweries in breweries_response["breweries"] if breweries["areaId"]==areaId]
    select_breweries = st.sidebar.selectbox("好きな蔵元を選んでください", breweries)
    # 蔵元IDを取得
    breweryId = [breweries["id"] for breweries in breweries_response["breweries"] if breweries["name"]==select_breweries][0]
    # 銘柄名を取得
    brands_response = requests.get(urls.get("銘柄一覧")).json()
    brands = [brands["name"] for brands in brands_response["brands"] if brands["breweryId"]==breweryId]
    select_brands = st.sidebar.selectbox("好きな銘柄を選んでください", brands)
    # 銘柄IDを取得
    brandId = [brands["id"] for brands in brands_response["brands"] if brands["name"]==select_brands][0]
    # フレーバーチャートを取得
    flavor_charts_response = requests.get(urls.get("フレーバーチャート")).json()
    flavor_charts = [flavor_charts for flavor_charts in flavor_charts_response["flavorCharts"] if flavor_charts["brandId"]==brandId]
    # plotlyでレーダーチャートを表示
    st.markdown(f'## {select_brands}のフレーバーチャート')
    try:
        df = pd.DataFrame(flavor_charts)
        df = df.drop('brandId', axis=1)
        # 見やすくするためにカラム名を変更、その後plotlyで読み込めるようにデータを転置
        df = df.rename(columns={'f1':'華やか', 'f2':'芳醇', 'f3':'重厚', 'f4':'穏やか', 'f5':'ドライ', 'f6':'軽快'}).T
        fig = px.line_polar(df, r=df[0], theta=df.index, line_close=True, range_r=[0,1])
        st.plotly_chart(fig)
    # フレーバーチャートのデータがないものもあるので例外処理
    except:
        st.markdown('## この銘柄はフレーバーチャートを表示できません！！')
        
if __name__=='__main__':
    sake()
