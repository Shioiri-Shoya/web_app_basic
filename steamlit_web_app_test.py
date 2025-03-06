# Run this app with `streamlit run steamlit_web_app.py` and
# visit http://localhost:8501 in your web browser.

# 以下のライブラリを使用するため、事前にターミナル（コマンドプロンプト）でインストールしてください。

import pandas as pd
import numpy as np
matplotlib.use('Agg')  # Streamlit でのバックエンド指定
import matplotlib.pyplot as plt
import scipy.stats as stats
import streamlit as st
import plotly.express as px

# Q: 以下の...部分を埋めて、コードを完成させてください。 

# 最後に作成する main 関数を実行することで、Streamlit を起動させます。
# すべての実行プロセスを main 関数内に含めてしまうと、エラーの原因が分かりにくくなったり、コードが読みにくくなったりするため、作成が困難になります。
# そのため、main 関数内で使用する関数をあらかじめ作成しておくことで、コードを見やすくし、間違いにも気づきやすくすることができます。
# まずは、Q1～Q3 で 3 つの関数を作成していきましょう。

# Q1: データを前処理する関数 preprocess_data を作成してください。
def preprocess_data(dataset_path):
    dataset = pd.read_csv(dataset_path)

    # 外れ値の削除
    dataset = dataset.drop(dataset.index[[..., ...]]).reset_index(drop=True)
    dataset = dataset.drop(dataset.index[[..., ..., ...]]).reset_index(drop=True)

    # 欠損値を平均値で補完
    dataset['weight'].fillna(dataset['...'], inplace=True)

    # price_type の表記ゆれ修正
    dataset['price_type'] = dataset['price_type'].replace({'通常価格': '...', '割引価格': '...'})

    # price_type と item_type をダミー変数化
    dataset = pd.get_dummies(dataset, columns=[..., ...])

    # occupancy を小数に変換
    dataset['occupancy'] = dataset['occupancy'].str.replace('%', '').astype(...)

    return dataset

# Q2: 1標本t検定を行う関数 one_sample_t_test を作成してください。
def one_sample_t_test(dataset, column, popmean):
    t_stat, p_value = stats.ttest_1samp(dataset[column], ..., alternative='greater')
    return f"t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}"

# Q3: 2標本t検定を行う関数 two_sample_t_test を作成してください。
def two_sample_t_test(df_a, df_b, column='purchase_price'):
    t_stat, p_value = stats.ttest_ind(df_a[column], df_b[column])
    return f"t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}"

# Streamlit アプリ
def main():
    # Q5: Streamlit のタイトル機能を使い、タイトルを作成してください。
    ...

    # Q6: Streamlit のタブ機能を使い、'Eラーニングデータ分析'と'小売店舗ビジネスデータ分析'の2つのタブを作成してください。
    tab1, tab2 = ...

    # Eラーニングタブ
    with tab1: 
        # Q7: Streamlit のヘッダー作成機能を使い、'Eラーニングデータ分析'のヘッダーを作成してください。
        ... 

        # Q8: 以下の3つのデータセットを読み込んでください。
        student_info = ...
        module_assessments = ...
        student_assessment = ...

        # Q9: code_module ごとの受講生数を棒グラフで可視化してください。
        st.subheader('code_module ごとの受講生数')
        student_info_groupby_code_module = student_info.groupby('...')['...'].count().reset_index()
        fig1 = px.bar(student_info_groupby_code_module, x='...', y='...', title='code_moduleごとの受講生数')
        ... # Streamlitの機能を用いてグラフを表示させる。

        # Q10: 'CCC', '2014J', 'Exam' のスコアの分布をヒストグラムで表示してください。
        st.subheader('モジュールCCC, プレゼンテーション2014JのExamスコア')
        assessments = pd.merge(student_assessment, ..., on='...', how='left')
        assessments_CCC_2014J_Exam = assessments.query(
            'code_module == "..." and code_presentation == "..." and assessment_type == "..."'
        ).reset_index(drop=True)
        fig2 = px.histogram(assessments_CCC_2014J_Exam, x='...', nbins=..., title='Examスコアの分布')
        ... # Streamlitの機能を用いてグラフを表示させる

        # Q11: final_result ごとの合計スコアを箱ひげ図で可視化してください。
        st.subheader('最終結果ごとの合計スコア')
        assessments['weight_score'] = assessments['score'] * assessments['weight'] / ...
        student_total_score = assessments.groupby([...]) \
            .agg({'weight_score': np.sum}) \
            .rename(columns={'weight_score': '...'}) \
            .reset_index()
        student_info_with_total_score = pd.merge(student_info, student_total_score, on=[..., ..., ...], how='right')

        fig3 = px.box(
            student_info_with_total_score, x='final_result', y='total_score',
            category_orders={'final_result': [..., ..., ..., ...]},
            title='最終結果と合計スコアの関係'
        )
        ... # Streamlitの機能を用いてグラフを表示させる

    # 小売店舗ビジネスタブ
    # Q12: Eラーニングタブを参考に、小売店舗ビジネスタブを完成させて下さい。
    # ただし、作成した関数、preprocess_data、one_sample_t_test、two_sample_t_test全てを用いること。
    # また、以下の３つの項目を満たすように作成して下さい。
    # ① purchase_price のヒストグラムの表示
    # ② 1標本t検定を実装し、ボタンを押すと結果が表示
    # ③ 2標本t検定を実装し、A社とB社の purchase_price を比較

if __name__ == '__main__':
    main()