import streamlit as st
import pandas as pd
# 実装予定
# import matplotlib.pyplot as plt
# import japanize_matplotlib
from scipy import stats
from PIL import Image
from statistics import median, variance

st.set_page_config(page_title="ブラウザt検定(対応あり)", layout="wide")

st.title("ブラウザt検定(対応あり)")
st.caption("Created by Daiki Ito")
st.write("")
st.subheader("ブラウザでt検定　→　表　→　解釈まで出力できるウェブアプリです。")
st.write("iPad等でも分析を行うことができます")
st.write("")

st.subheader("【注意事項】")
st.write("excelファイルに不備があるとエラーが出ます")
st.write('<span style="color:blue">デフォルトでデモ用データの分析ができます。</span>',
         unsafe_allow_html=True)
st.write(
    '<span style="color:blue">ファイルをアップせずに「データフレームの表示」ボタンを押すと　'
    'デモ用のデータを確認できます。</span>',
    unsafe_allow_html=True)
st.write('<span style="color:red">欠損値を含むレコード（行）は自動で削除されます。</span>',
         unsafe_allow_html=True)

code = '''
#使用ライブラリ
import streamlit as st
import pandas as pd
from scipy import stats
from PIL import Image
from statistics import median, variance
'''

st.code(code, language='python')

# Excelデータの例
image = Image.open('ttest_rel.png')
st.image(image)

# 使い方動画
# video_file = open('雨音子.mp4', 'rb')  # 動画はテスト
# video_bytes = video_file.read()
# st.video(video_bytes)

# デモ用ファイル
df = pd.read_excel('ttest_rel_demo.xlsx', sheet_name=0)

# xlsxファイルのアップロード
upload_files_xlsx = st.file_uploader("ファイルアップロード", type='xlsx')

# xlsxファイルの読み込み → データフレームにセット
if upload_files_xlsx:
    # dfを初期化
    df.drop(range(len(df)))
    # xlsxファイルの読み込み → データフレームにセット
    df = pd.read_excel(upload_files_xlsx, sheet_name=0)
    # 欠損値を含むレコードを削除
    df.dropna(how='any', inplace=True)

# データフレーム表示ボタン
if st.checkbox('データフレームの表示'):
    st.dataframe(df, width=0)

# 変数選択フォーム
with st.form(key='variable_form'):
    st.subheader("分析に使用する変数（観測値、測定値）の選択")

    # 観測値と測定値のセット
    ovList = df.columns.tolist()
    mvList = df.columns.tolist()

    # 複数選択（観測値）
    ObservedVariable = st.multiselect(
        '観測値（複数選択可）',
        ovList)

    # 複数選択（観測値）
    MeasuredVariable = st.multiselect(
        '測定値（複数選択可）',
        mvList)

    st.write(
        '<span style="color:blue">【注意】従属変数に数値以外のものがある場合、分析できません</span>',
        unsafe_allow_html=True)
    
    # 変数の個数があってないときの処理
    ovRange = len(ObservedVariable)
    mvRange = len(MeasuredVariable)

    if ovRange != mvRange:
        st.write("観測値の数と測定値の数を合わせてください")
    else:
        st.write("分析可能です")


    # 確認ボタンの表示
    CHECK_btn = st.form_submit_button('確認')

# 分析前の確認フォーム
with st.form(key='check_form'):
    if CHECK_btn:
        st.subheader('【分析前の確認】')

        n = 0
        ovRangeView = len(ObservedVariable)
        mvRangeView = len(MeasuredVariable)
        for dvListView in range(ovRangeView):
            st.write(f'● 【'f'{(ObservedVariable[n])}'f'】　→　【'f'{(MeasuredVariable[n])}】')
            n += 1
        st.write('　に有意な差が生まれるか検定します。')

    # 分析実行ボタンの表示
    TTEST_btn = st.form_submit_button('分析実行')

# 分析結果表示フォーム
with st.form(key='analyze_form'):
    if TTEST_btn:
        st.subheader('【分析結果】')
        st.write('【要約統計量】')

        # 各値の初期化
        n = 1
        
        # リストの名前を取得
        summaryList = []
        for sl in range(ovRangeView):
            summaryList.append(f'● 【'f'{(ObservedVariable[n])}'f'】　→　【'f'{(MeasuredVariable[n])}】')
            ovRangeView += 1

            
        summaryColumns = ["有効N", "平均値", "中央値", "標準偏差", "分散",
                          "最小値", "最大値"]

        # 観測値、測定値から作業用データフレームのセット
        df00_list = [ObservedVariable]
        df00_list = df00_list + MeasuredVariable
        df00 = df[df00_list]


        # サマリ(df0)用のデータフレームのセット
        df0 = pd.DataFrame(index=summaryList, columns=summaryColumns)


        # サマリ(df0)用のデータフレームに平均値と標準偏差を追加
        for summary in range(ovRange):
            # 列データの取得（nは従属変数の配列番号）
            y = df00.iloc[:, n]

            # 従属変数の列データの計算処理
            df0.at[df00.columns[n], '有効N'] = len(y)
            df0.at[df00.columns[n], '平均値'] = y.mean()
            df0.at[df00.columns[n], '中央値'] = median(y)
            df0.at[df00.columns[n], '標準偏差'] = y.std()
            df0.at[df00.columns[n], '分散'] = variance(y)
            df0.at[df00.columns[n], '最小値'] = y.min()
            df0.at[df00.columns[n], '最大値'] = y.max()
            n += 1

        # 要約統計量（サマリ）のデータフレームを表示
        st.dataframe(df0)

        st.write('【平均値の差の検定】')

        # 各値の初期化
        n = 1

        st.write(summaryList)
    
'''
        # t検定結果用データフレーム（df1）の列を指定
        summaryColumns = ['全体M', '全体S.D', DivideVariable[0] + "M",
                          DivideVariable[0] + "S.D", DivideVariable[1] + "M",
                          DivideVariable[1] + "S.D", 'df', 't', 'p', 'sign',
                          'd']
        df1 = pd.DataFrame(index=summaryList, columns=summaryColumns)

        for summary in range(dvRange):
            # 列データの取得（nは従属変数の配列番号）
            y = df00.iloc[:, n]

            # df（元データ）男性でフィルターしたデータフレームをセット
            dv0 = df00[df00[IndependentVariable] == DivideVariable[0]]
            dv1 = df00[df00[IndependentVariable] == DivideVariable[1]]

            # フィルターした列データの取得（nは従属変数の配列番号）
            dv0y = dv0.iloc[:, n]
            dv1y = dv1.iloc[:, n]

            # t値、p値、s（全体標準偏差）、d値（効果量）の取得
            ttest = stats.ttest_ind(dv0y, dv1y, equal_var=False)
            t = abs(ttest[0])
            p = ttest[1]
            s = y.std()
            dv0ym = dv0y.mean()
            dv1ym = dv1y.mean()
            d_beta = dv0ym - dv1ym
            d = abs(d_beta) / s

            # p値の判定をsignに格納
            sign = ""
            if p < 0.01:
                sign = "**"
            elif p < 0.05:
                sign = "*"
            elif p < 0.1:
                sign = "†"
            else:
                sign = "n.s."

            # 従属変数の列データの計算処理
            df1.at[df00.columns[n], '全体M'] = y.mean()
            df1.at[df00.columns[n], '全体S.D'] = y.std()
            df1.at[df00.columns[n], DivideVariable[0] + "M"] = dv0y.mean()
            df1.at[df00.columns[n], DivideVariable[0] + "S.D"] = dv0y.std()
            df1.at[df00.columns[n], DivideVariable[1] + "M"] = dv1y.mean()
            df1.at[df00.columns[n], DivideVariable[1] + "S.D"] = dv1y.std()
            df1.at[df00.columns[n], 'df'] = len(y) - 1
            df1.at[df00.columns[n], 't'] = t
            df1.at[df00.columns[n], 'p'] = p
            df1.at[df00.columns[n], 'sign'] = sign
            df1.at[df00.columns[n], 'd'] = d

            n += 1

        st.dataframe(df1)

        # サンプルサイズの取得
        sample_n = len(df00)
        sample_0 = len(dv0)
        sample_1 = len(dv1)

        st.write('【サンプルサイズ】')
        st.write(f'全体N ＝'f'{sample_n}')
        st.write(f'● {DivideVariable[0]}：'f'{sample_0}')
        st.write(f'● {DivideVariable[1]}：'f'{sample_1}')

        st.write('【分析結果の解釈】')

        # 各値の初期化、簡素化
        n = 0
        d0 = DivideVariable[0]
        d1 = DivideVariable[1]
        iv = IndependentVariable

        # sign の列番号を取得
        sign_n = df1.columns.get_loc('sign')
        # DivideVariable[0] + 'M' の列番号を取得
        d0n = df1.columns.get_loc(d0 + "M")
        # DivideVariable[1] + 'M' の列番号を取得
        d1n = df1.columns.get_loc(d1 + "M")

        for interpretation in range(dvRange):
            dn = DependentVariable[n]
            if df1.iat[n, sign_n] == "**":
                if df1.iat[n, d0n] > df1.iat[n, d1n]:
                    st.write(
                        f'{iv}によって【'f'{dn}】には有位な差が生まれる'f'（{d0}＞'f'{d1}）')
                elif df1.iat[n, d0n] < df1.iat[n, d1n]:
                    st.write(
                        f'{iv}によって【'f'{dn}】には有意な差が生まれる'f'（{d1}＞'f'{d0}）')
            elif df1.iat[n, sign_n] == "*":
                if df1.iat[n, d0n] > df1.iat[n, d1n]:
                    st.write(
                        f'{iv}によって【'f'{dn}】には有意な差が生まれる'f'（{d0}＞'f'{d1}）')
                elif df1.iat[n, d0n] < df1.iat[n, d1n]:
                    st.write(
                        f'{iv}によって【'f'{dn}】には有意な差が生まれる'f'（{d1}＞'f'{d0}）')
            elif df1.iat[n, sign_n] == "†":
                if df1.iat[n, d0n] > df1.iat[n, d1n]:
                    st.write(
                        f'{iv}によって【'f'{dn}】には有意な差が生まれる傾向にある'f'（{d0}＞'f'{d1}）')
                elif df1.iat[n, d0n] < df1.iat[n, d1n]:
                    st.write(
                        f'{iv}によって【'f'{dn}】には有意な差が生まれる傾向にある'f'（{d1}＞'f'{d0}）')
            elif df1.iat[n, sign_n] == "n.s.":
                st.write(f'{iv}によって【'f'{dn}】には有意な差が生まれない')

            n += 1

        TTEST_btn = st.form_submit_button('OK')

st.write('ご意見・ご要望は→', 'https://forms.gle/G5sMYm7dNpz2FQtU9', 'まで')
st.write('© 2022 Daiki Ito. All Rights Reserved.')

'''