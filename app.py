import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime,date,timedelta,timezone


def graph_plt():
    
    TITLE = "STREAMLIT TEST Ver.01"
    st.title(f"{TITLE}")

    #status_area = st.empty()
    # カウントダウン
    #count_down_sec = 5
    #for i in range(count_down_sec):
        # プレースホルダーに残り秒数を書き込む
        #status_area.write(f'あと{count_down_sec - i}秒 ')
        # スリープ処理を入れる
        #time.sleep(1)

    # 完了したときの表示
    #status_area.write('発射！！')
    # 風船飛ばす
    #st.balloons()

    #status_text = st.empty()
    # プログレスバー
    #progress_bar = st.progress(0)

    #for i in range(100):
        #status_text.text(f'進捗は{i}パーセント')
        # for ループ内でプログレスバーの状態を更新する
        #progress_bar.progress(i + 1)
        #time.sleep(0.1)

    #status_text.text('完了！！')

    # 折れ線グラフ (初期状態)
    #x = np.random.random(size=(10, 2))
    #line_chart = st.line_chart(x)

    #for i in range(15):
        # 折れ線グラフに 0.5 秒間隔で 15 回データを追加する
        #additional_data = np.random.random(size=(5, 3))
        #line_chart.add_rows(additional_data)
        #time.sleep(0.5)

    #f = st.file_uploader(label='ファイルのアップロード:')
    #st.write('選択されたファイル: ', f)

    #if f is not None:
        # XXX: 信頼できないファイルは安易に評価しないこと
        #data = f.getvalue()
        #text = data.decode('utf-8')
        #st.write('ファイルの内容：', text)

    
    UNOW=datetime.now()
    JST=timezone(timedelta(hours=+9))
    NOW=UNOW+timedelta(hours=+9)
    TIME=datetime(NOW.year,NOW.month,NOW.day,NOW.hour,NOW.minute,tzinfo=JST)
    STIME=TIME.strftime("%Y年%m月%d日%H時%M分")
    st.write(f"日本のコロナ感染者数推移{STIME}現在")
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
    #chart_data = pd.DataFrame(dfpcd)
    #折れ線グラフ (初期状態)
    #line_chart = st.line_chart(chart_data.iloc[100, :].T)
    #for i in range(1000):
        #折れ線グラフに 0.5 秒間隔で 15 回データを追加する
        #additional_data = chart_data.iloc[100+i,:].T
        #line_chart.add_rows(additional_data)
        #time.sleep(0.001)
    st.line_chart(chart_data)

    #st.table(chart_data)
    #csv = chart_data.to_csv(index=False)  

    # utf-8
    #b64 = base64.b64encode(csv.encode()).decode()
    #href = f'<a href="data:application/octet-stream;base64,{b64}" download="result_utf-8.csv">Download Link</a>'
    #st.markdown(f"CSVファイルのダウンロード(utf-8):  {href}", unsafe_allow_html=True)

    # utf-8(BOM)
    #b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
    #href = f'<a href="data:application/octet-stream;base64,{b64}" download="result_utf-8-sig.csv">Download Link</a>'
    #st.markdown(f"CSVファイルのダウンロード(utf-8 BOM):  {href}", unsafe_allow_html=True)

if __name__=='__main__':
    graph_plt()
