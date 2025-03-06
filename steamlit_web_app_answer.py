# Run this app with `streamlit run steamlit_web_app.py` and
# visit http://localhost:8501 in your web browser.

# 以下のライブラリを使用するため、事前にターミナル（コマンドプロンプト）でインストールしてください。

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import streamlit as st
import plotly.express as px

# Q: 以下の...部分を埋めて、コードを完成させてください。

# Q1: 小売店舗ビジネスデータを前処理する関数 preprocess_data を、「1-3_Pythonによる統計モデリング」で行った内容を参考にして作成してください。
def preprocess_data(dataset_path):
    dataset = pd.read_csv(dataset_path)

    # 外れ値の削除
    dataset = dataset.drop(dataset.index[[1, 7]]).reset_index(drop=True)
    dataset = dataset.drop(dataset.index[[218, 280, 409]]).reset_index(drop=True)

    # 欠損値補完
    dataset['weight'].fillna(dataset['weight'].median(), inplace=True)

    # price_type の表記ゆれ修正
    dataset['price_type'] = dataset['price_type'].replace({'通常価格': '定価', '割引価格': '割引'})

    # price_type と item_type をダミー変数化
    dataset = pd.get_dummies(dataset, columns=['price_type', 'item_type'])

    # occupancy を小数に変換
    dataset['occupancy'] = dataset['occupancy'].str.replace('%', '').astype(float)

    return dataset

# Q2: 1標本t検定を行う関数 one_sample_t_test を作成してください。
def one_sample_t_test(dataset, column, popmean):
    t_stat, p_value = stats.ttest_1samp(dataset[column], popmean, alternative='greater')
    return f"t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}"

# Q3: 2標本t検定を行う関数 two_sample_t_test を作成してください。
def two_sample_t_test(df_a, df_b, column='purchase_price'):
    t_stat, p_value = stats.ttest_ind(df_a[column], df_b[column])
    return f"t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}"

# Streamlit アプリ
def main():
    # Q5: Streamlit のタイトル機能を使い、タイトルを作成してください。
    st.title('Eラーニングデータ分析 & 小売店舗ビジネスデータ分析')

    # Q6: Streamlit のタブ機能を使い、'Eラーニングデータ分析'と'小売店舗ビジネスデータ分析'の2つのタブを作成してください。
    tab1, tab2 = st.tabs(['Eラーニングデータ分析', '小売店舗ビジネスデータ分析'])

    # Eラーニングタブ
    with tab1:
        # Q7: Streamlit のヘッダー作成機能を使い、'Eラーニングデータ分析'のヘッダーを作成してください。
        st.header('Eラーニングデータの分析')

        # Q8: 以下の3つのデータセットを読み込んでください。
        student_info = pd.read_csv('dataset/student_info.csv')
        module_assessments = pd.read_csv('dataset/module_assessments.csv')
        student_assessment = pd.read_csv('dataset/student_assessment.csv')

        # Q9: code_module ごとの受講生数を棒グラフで可視化してください。
        st.subheader('code_module ごとの受講生数')
        student_info_groupby_code_module = student_info.groupby('code_module')['id_student'].count().reset_index()
        fig1 = px.bar(student_info_groupby_code_module, x='code_module', y='id_student', title='code_moduleごとの受講生数')
        st.plotly_chart(fig1)

        # Q10: 'CCC', '2014J', 'Exam' のスコアの分布をヒストグラムで表示してください。
        st.subheader('モジュールCCC, プレゼンテーション2014JのExamスコア')
        assessments = pd.merge(student_assessment, module_assessments, on='id_assessment', how='left')
        assessments_CCC_2014J_Exam = assessments.query(
             'code_module == "CCC" and code_presentation == "2014J" and assessment_type == "Exam"'
             ).reset_index(drop=True)
        fig2 = px.histogram(
            assessments_CCC_2014J_Exam, 
            x='score', 
            nbins=30, 
            title='Examスコアの分布'
            )
        st.plotly_chart(fig2)
    
        # Q11: final_result ごとの合計スコアを箱ひげ図で可視化してください。
        st.subheader('最終結果ごとの合計スコア')
        assessments['weight_score'] = assessments['score'] * assessments['weight'] / 100
        student_total_score = assessments.groupby(['id_student', 'code_module', 'code_presentation']) \
            .agg({'weight_score': np.sum}) \
            .rename(columns={'weight_score': 'total_score'}) \
            .reset_index()
        student_info_with_total_score = pd.merge(student_info, student_total_score, on=['id_student', 'code_module', 'code_presentation'], how='right')

        fig3 = px.box(
            student_info_with_total_score, x='final_result', y='total_score',
            category_orders={'final_result': ['Withdrawn', 'Fail', 'Pass', 'Distinction']},
            title='最終結果と合計スコアの関係'
        )
        st.plotly_chart(fig3)

    # 小売店舗ビジネスタブ
    # Q12: Eラーニングタブを参考に、小売店舗ビジネスタブを完成させて下さい。
    # ただし、作成した関数、preprocess_data、one_sample_t_test、two_sample_t_test全てを用いること。
    # また、以下の３つの項目を満たすように作成して下さい。
    # ① purchase_price のヒストグラムの表示
    # ② 1標本t検定を実装し、ボタンを押すと結果が表示
    # ③ 2標本t検定を実装し、A社とB社の purchase_price を比較（「1-3_Pythonによる統計モデリング」の「2-2. 2標本のt検定」で行ったことを参考にしてください。）
    
    with tab2:
        st.header('小売店舗ビジネスデータの分析')

        dataset_path = 'dataset/dataset.csv'
        dataset = preprocess_data(dataset_path)

        # purchase_price のヒストグラムの表示
        st.subheader('purchase_price のヒストグラム')
        fig = px.histogram(dataset, x='purchase_price', nbins=30, title='purchase_price の分布')
        fig.update_traces(marker=dict(line=dict(color='black', width=1)))  # 境界線を追加
        fig.update_layout(bargap=0.1)  # バーの間隔調整
        st.plotly_chart(fig)

        # 1標本t検定を実装し、ボタンを押すと結果が表示
        st.subheader('1標本t検定')
        popmean = st.number_input('比較する平均値（popmean）', min_value=0, value=70)
        if st.button('検定を実行'):
            result = one_sample_t_test(dataset, 'purchase_price', popmean)
            st.write(result)

        # 2標本t検定を実装し、A社とB社の purchase_price を比較
        st.subheader('2標本t検定')
        if st.button('A社 vs B社 の purchase_price を比較'):
            purchese_price_from_a = pd.DataFrame([
                ['ID_DN23', 93], ['ID_DO11',159], ['ID_DO23',38], ['ID_DP11',96],
                ['ID_DP23',106], ['ID_DP59',97], ['ID_DQ11',82], ['ID_DQ23',88]
            ], columns=['item_id', 'purchase_price'])

            purchese_price_from_b = pd.DataFrame([
                ['ID_DH26', 83], ['ID_DH50', 79], ['ID_DI14', 87], ['ID_DI26', 68]
            ], columns=['item_id', 'purchase_price'])

            result = two_sample_t_test(purchese_price_from_a, purchese_price_from_b)
            st.write(result)

if __name__ == '__main__':
    main()

 