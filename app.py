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

st.write(f'<span style="font-size:xx-large;font-weight:bolder">日本酒AIソムリエ</span>',unsafe_allow_html=True)
#col1,col2,col3= st.columns(3)
#col1.image("image/sake1.jpg", use_column_width=True)
st.write(f'<span style="font-size:small">[さけのわ様のAPI](https://sakenowa.com)を使用しています</span>',unsafe_allow_html=True)

#エンドポイント
urls = {
"地域一覧": "https://muro.sakenowa.com/sakenowa-data/api/areas",
"銘柄一覧": "https://muro.sakenowa.com/sakenowa-data/api/brands",
"蔵元一覧": "https://muro.sakenowa.com/sakenowa-data/api/breweries",
"フレーバーチャート": "https://muro.sakenowa.com/sakenowa-data/api/flavor-charts",
"ランキング": "https://muro.sakenowa.com/sakenowa-data/api/rankings"
}

#データフレーム作成
@st.cache
def get_df(urlname,key) :
  dic = requests.get(urls.get(urlname)).json()
  df = pd.DataFrame(dic[key]).set_index('id')
  return df

# フレーバーチャートを取得
@st.cache
def get_flavor_charts_response():
  flavor_charts_response = requests.get(urls.get("フレーバーチャート")).json()
  return flavor_charts_response

#ランキング取得
def get_rank(urlname,key,brandId):
    rank_response = requests.get(urls.get(urlname)).json()
    ranking=pd.DataFrame(rank_response[key]).query('brandId==@brandId')['rank'].values[0]
    return ranking

def sake():

  df_area=get_df("地域一覧","areas")
  areaId=st.sidebar.selectbox("好きな地域を選んでください",df_area.index.values,format_func=lambda x:df_area.loc[x,"name"])

  df=get_df("蔵元一覧","breweries")
  df_brewery=df[df["areaId"]==areaId]
  breweryId = st.sidebar.selectbox("好きな蔵元を選んでください",df_brewery.index.values,format_func=lambda x:df_brewery.loc[x,"name"])
  
  #銘柄名を取得
  df=get_df("銘柄一覧","brands")
  df_brand = df[df["breweryId"] == breweryId]["name"]
  select_brands = st.sidebar.selectbox("好きな銘柄を選んでください",df_brand.values )
  
  #ここをコールバック関数で書きたい
  #セレクトボックスとテキストボックスを比較して違ってたら、テキストボックスの内容を反映
  text = st.text_input('選ぶお酒：',select_brands )
  if select_brands !=  text:
    select_brands = text
  # 銘柄IDを取得
  'あなたが選んだお酒は「',text,'」です。'
    #銘柄IDを取得
  brandId = df[df['name']==select_brands].index
  
  # フレーバーチャートを取得
  flavor_charts_response = get_flavor_charts_response()
  flavor_charts = [flavor_charts for flavor_charts in flavor_charts_response["flavorCharts"] if flavor_charts["brandId"]==brandId]
  
  # plotlyでレーダーチャートを表示
  if st.checkbox("フレーバーチャートを表示") :
    try:
      df = pd.DataFrame(flavor_charts)
      df = df.drop('brandId', axis=1)
      # 見やすくするためにカラム名を変更、その後plotlyで読み込めるようにデータを転置
      df = df.rename(columns={'f1':'華やか', 'f2':'芳醇', 'f3':'重厚', 'f4':'穏やか', 'f5':'ドライ', 'f6':'軽快'}).T
      fig = px.line_polar(df, r=df[0], theta=df.index, line_close=True, range_r=[0,1],width=350,height=350)
      left_column,mid,right_column = st.columns(3)
      left_column.plotly_chart(fig)         
    except:
      st.write(f'<span style="color:red;background:pink">この銘柄はフレーバーチャートを表示できません！！</span>',unsafe_allow_html=True)  

  if st.checkbox("全国ランキングを表示") :
    try:
      #ランキングデータフレーム
      brandId=brandId.values[0]
      ranking=get_rank('ランキング','overall',brandId)
      st.write(f'<span style="font-size:medium">「{text}」の全国ランキングは{ranking}位です。</span>',unsafe_allow_html=True)
    except:
      st.write(f'<span style="color:red;background:pink">この銘柄は全国ランキングを表示できません！！</span>',unsafe_allow_html=True)
      
  if st.checkbox("県内ランキングを表示") :
    try:
      #ランキングデータフレーム
      brandId=brandId.values[0]
      ranking=get_rank('ランキング','area',brandId)
      st.write(f'<span style="font-size:medium">「{text}」の同県内でのランキングは{ranking}位です。</span>',unsafe_allow_html=True)
    except:
      st.write(f'<span style="color:red;background:pink">この銘柄は県内ランキングを表示できません！！</span>',unsafe_allow_html=True)
      
if __name__=='__main__':
      sake()
