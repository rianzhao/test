# numpy, pandas, matplotlib practice

# Watch those materials

# numpy tutorial: https://www.w3schools.com/python/numpy_intro.asp

# pandas tutorial: https://www.youtube.com/watch?v=PfVxFV1ZPnk

# funtional programming youtube video: https://www.youtube.com/watch?v=goypZR_lQ7I

# matplotlib tutorial: https://matplotlib.org/tutorials/index.html




# practice:

# 首先熟悉resources 下面是不同的人对于不同电影的评分，分别存储在几个不同的文件里。每个文件头上是各个栏的TITLE。
# 其次通过数据处理，进行数据的合并，生成一个EXCEL表格，将用户评分的如下信息列出来。注意有的客户可能对几个不同的电影打分，并且有可能对同一个电影进行多次评分。
# EXCEL表格内容包括  用户基本信息 （id, 名字，职业，电影名，电影类别，评分，打分日期）
# 通过图标进行一些简单的数据分析，例如，什么从用户角度，什么职业的人最多，用户评分最多是什么，再比如，从电影角度，哪种类型的电影最受欢迎，等等

import openpyxl
import xlwt
import pandas as pd
pd.set_option('display.max_columns', None)

df_data = pd.read_csv('u.data', sep='\t')
df_user = pd.read_csv('u.user', sep='|')
df_item = pd.read_csv('u.item', sep='|')

df_data_user = pd.merge(df_data, df_user, left_on='user id ', right_on='user id ', how='inner')

df_data_user_item = pd.merge(df_data_user, df_item, left_on=' item id ', right_on='movie id ', how='inner')

df = df_data_user_item.drop(' IMDb URL ', axis=1)
df.to_excel('df_data_user_item.xlsx')
print(df)

#