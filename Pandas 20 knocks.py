# これはPandasフレームワークの20本ノックです。
# 以下のURLの問題について記載しております。
# https://www.youtube.com/watch?v=ZQZ38rK28Gk

#　インポート、warnings非表示
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


# Q1.データの読み込み
df = pd.read_csv('weather.csv')


# Q2.先頭3行、末尾10行確認
print(df.head(3))
print(df.tail(10))


# Q3.不要な列の削除、0行目の削除
print(df.columns)
df = df[['年月日',
         '平均気温(℃)',
         '最高気温(℃)',
         '最低気温(℃)',
         '降水量の合計(mm)',
         '最深積雪(cm)',
         '平均雲量(10分比)',
         '平均蒸気圧(hPa)',
         '平均風速(m/s)',
         '日照時間(時間)'
              ]][1:] #列を省略することもできる。
print(df.head(3))

# df.columns=にしたらコラムの数を合わせろというエラーが出る。


# Q4.各列のデータ型、サイズ、列名、行名の確認
print(df.dtypes)
print(df.shape) # (行の数, 列の数)で結果が表示される。
print(df.columns)
print(df.index)


# Q5.df5~10行目、3~6列目（最高気温(℃)~最新積雪(cm)）を取得
# iloc
df_1 = df.iloc[4:10,2:6] #（行, 列）　始まりは一個前の数
print(df_1)
#loc
df_2 = df.loc[5:10,"最高気温(℃)":"最深積雪(cm)"]
print(df_2)


# Q6.条件抽出　people.csv読み込み、nationalityがAmerica、ageが20以上で30未満のデータ抽出
df_people = pd.read_csv("people.csv")

# 条件式
df_people_1 = df_people[df_people["nationality"]=="America"]
print(df_people_1)
df_people_2 = df_people[(df_people["age"]>=20) & (df_people["age"]<30)]
print(df_people_2)

#　query
df_people_1 = df_people.query("nationality == 'America'")
print(df_people_1)
df_people_2 = df_people.query("age >= 20 & age < 30")
print(df_people_2)

# isin nationalityがAmericaであるもののみ抽出する方法
df_people_1 = df_people[df_people["nationality"].isin(["America"])] # isinの後注意　isin(["検索文字"])


# Q7.コラム（列）ごとのユニークな値の抽出
print(df_people.columns)
age_unique = df_people["age"].unique()
print(age_unique)
name_unique = df_people["name"].unique()
print(name_unique)
nationality_unique = df_people["nationality"].unique()
print(nationality_unique)


# Q8.重複除去　nationalityの列に対して、重複のある行は削除　各国代表1人ずつ
print(df_people.head(3))
nationality_non_dup = df_people.drop_duplicates(subset="nationality")
print("nationality_non_dup",nationality_non_dup)

# 全てのコラムが全く同じもののみ削除する場合は、subsetを指定しない。


# Q9.コラム名変更、単位を消す
print(df.columns)
df.columns = ['年月日',
              '平均気温',
              '最高気温',
              '最低気温',
              '降水量の合計',
              '最深積雪',
              '平均雲量',
              '平均蒸気圧',
              '平均風速',
              '日照時間']
print(df.columns)
# 上記はコラムの数を合わせる必要有り
# 一つだけ変える場合はrenameでも可能
df = df.rename(columns={"年月日": "年/月/日"})
print(df.columns)


# Q10.並び替え　dfを最高気温の高い順にする。
print(df.head(3))
df = df.sort_values("最高気温",ascending=False)
print(df.head(3))

#デフォルトは小さいものから並ばれる。


# Q11. ダミー変数の処理 nationality コラムをダミー変数にする。
print(df_people.head(3))
dummy = pd.get_dummies(df_people, columns=["nationality"]) 
#get_dummies(データフレーム, ダミー変数にしたいコラム名)
print(dummy)


# Q12.欠損値の確認
print("欠損値確認",df.isnull()) #Trueが欠損値


# Q13. 欠損値の補完　0で補完する。
df_fill = df.fillna(0) #各列のデータ型に合わせて補完される。(Float型かint型)
print(df_fill)
# 平均値で補完する場合 
df_fill = df.fillna(df.mean())
print(df_fill) #全ての値が欠損している場合はNaNが残るので注意。


# Q14. 欠損値の削除。列（縦）方向に削除。
print(df)
df_drop = df.dropna(axis=1) #行方向はaxis=0
print(df_drop)


# Q15. ユニークな値と出現回数　
df_iris = pd.read_csv("iris.csv")
print(df_iris.columns)
value_counts = df_iris["Class"].value_counts()
print(value_counts)

# Q16. グループごとの集計 Iris-versicolor,Iris-virginica, Iris-setosa 夫々の平均値。
groupby = df_iris.groupby("Class").mean()
print(groupby)


# Q17.　統計量の確認
print("平均値", df_iris.mean())
print("中央値", df_iris.median())
print("最頻値", df_iris.mode())
print("標準偏差", df_iris.std())
print("最大値", df_iris.max())
print("最小値", df_iris.min())
print("基本統計量", df_iris.describe())


# Q18. 折れ線グラフの表示 描画時にpasdasの裏側で使用されているので、matplotlibをインポートする必要が有る。
import matplotlib.pyplot as plt
print(df.head(3))
df = df.sort_values("年/月/日", ascending=True) #記載しなくてもdefaltでascending=True
print(df.head(3))
df.plot(x="年/月/日", y=["平均気温", "最高気温"], legend=False)


# Q19.　相関係数の算出　対象コラム：平均気温、降水量の合計、日照時間
print(df.columns)
corr = df[["平均気温","降水量の合計","日照時間"]].corr()
print(corr)
#　全部の相関関係を調べる場合
print(df.corr())


# Q20. データの出力 欠損値0で補完後、csvにて出力、indexは不要。
df = df.fillna(0)
df.to_csv("export.csv", index=False)











