# mysql installation tutorial : https://www.dev2qa.com/how-to-use-mysql-on-mac/

# **** (use if needed) **** python set to 3.7.3 in mac: https://opensource.com/article/19/5/python-3-default-mac

# Python mysql tutorial: https://www.w3schools.com/python/python_mysql_getstarted.asp

# TODO : design table schema, put resources/customer_rating_movies into 6 tables in local mysql database using python programming
import mysql.connector
import csv
import numpy as np

mydb = mysql.connector.connect(
  host='127.0.0.1',
  user='root',
  password='Spring2019',
  database='mydatabase'
)

mycursor=mydb.cursor(buffered=True)

occupation_schema = 'CREATE TABLE IF NOT EXISTS occupation (' \
                    'id INT AUTO_INCREMENT PRIMARY KEY, occu_name VARCHAR(255))'

user_schema = 'create table if not exists user (' \
              'user_id INT AUTO_INCREMENT PRIMARY KEY, ' \
              'age INT UNSIGNED, gender VARCHAR(255),occupation_id INT,zip_code VARCHAR(255), ' \
              'foreign key(occupation_id) references occupation(id))'

genre_schema = 'create table if not exists genre' \
                 '(type VARCHAR(255),' \
                 'id INT PRIMARY KEY)'

info_schema = 'create table if not exists info' \
                 '(num INT,' \
                 'type VARCHAR(255) PRIMARY KEY)'

item_schema = 'create table if not exists item' \
                 '(movie_id INT AUTO_INCREMENT PRIMARY KEY,' \
                 'movie_title VARCHAR(255),' \
                 'release_date VARCHAR(255),' \
                 'video_release_date VARCHAR(255),' \
                 'IMDB_URL VARCHAR(255),' \
                 'genre_id int(255),' \
                 'foreign key (genre_id) references genre(id))'

data_schema = 'create table if not exists data' \
                 '(id INT AUTO_INCREMENT PRIMARY KEY,' \
                 'user_id INT(11), ' \
                 'item_id INT(11), ' \
                 'rating TINYINT CHECK (rating >= 1 and rating <= 5),' \
                 'timestamp varchar(255),' \
                 'foreign key (user_id) references user(user_id),' \
                 'foreign key (item_id) references item(movie_id))'

occu='INSERT INTO occupation (occu_name) VALUE (%s)'

dat='INSERT INTO data (user_id, item_id, rating, timestamp) VALUES (%s, %s, %s,%s)'

use='INSERT INTO user (user_id, age, gender, occupation_id, zip_code) VALUES (%s, %s, %s, %s, %s)'

gen='INSERT INTO genre (type, id) VALUES (%s, %s)'

info='INSERT INTO info (num, type) VALUES (%s, %s)'

ite='INSERT INTO item (movie_title, release_date, video_release_date, IMDB_URL, genre_id) ' \
    'VALUES (%s, %s, %s, %s, %s)'


# table cleaning for fresh generation and data insert
def truncate_tables():
    foreign_key_sql_0 = 'SET FOREIGN_KEY_CHECKS = 0;'
    mycursor.execute(foreign_key_sql_0)
    mycursor.execute("show tables")
    tables = mycursor.fetchall()
    for table in tables:
        truncate_sql = 'truncate ' + table[0]
        mycursor.execute(truncate_sql)
    foreign_key_sql_1 = 'SET FOREIGN_KEY_CHECKS = 1;'
    mycursor.execute(foreign_key_sql_1)
    print("tables cleaned")


truncate_tables()


# start table creation and data insert
def create_table(schema, name):
    mycursor.execute(schema)
    print('table ' + name + ' created')


def read_file(name, delimiter):
    with open(name, newline='') as f:
        reader = csv.reader(f, delimiter=delimiter)
        data = list(reader)
    return data


def find_occu_Id(occu_name):
    sql_find_occu_id = 'select id from occupation where occu_name="'+ occu_name + '"'
    mycursor.execute(sql_find_occu_id)
    record = mycursor.fetchone()
    return record[0]


def find_gen_id(genre):
    sql_find_occu_id = 'select id from genre where type="' + genre + '"'
    mycursor.execute(sql_find_occu_id)
    record = mycursor.fetchone()
    return record[0]


def load_data(sql, source, delimiter):
    prefix = './resources/customers_rating_movies_data/'
    data_to_load = read_file(prefix + source, delimiter)
    if source == 'u.occupation' or source == 'u.genre' :
        mycursor.executemany(sql, data_to_load)
        mydb.commit()
    elif source == 'u.user':
        data_copy_to_load = data_to_load[1:]
        for row in data_copy_to_load:
            occu_id = str(find_occu_Id(row[3]))
            row[3] = occu_id
            mycursor.execute(sql, row)
        mydb.commit()
    elif source == 'u.item':
        title = data_to_load[0]
        movie_detail = data_to_load[1:]
        for detail in movie_detail:
            index_list = np.nonzero([int(i) for i in detail[5:]])[0]
            for i in index_list:
                genre_id = find_gen_id(title[i + 5].strip())
                detail = detail[1:5] + [genre_id]
                mycursor.execute(sql, detail)
        mydb.commit()
    elif source == 'u.data':
        data_to_load = data_to_load[1:]
        data_modified = []
        for row in data_to_load:
            data_modified.append([int(row[0])] + [int(row[1])] + [int(row[2])] + [row[3]])
        mycursor.executemany(sql, data_modified)
        mydb.commit()
    else:
        print('not recognize the source, return.')
        return


table_list = [
    {'schema': occupation_schema, 'name': 'occupation', 'sql': occu, 'delimiter': ','},
    {'schema': user_schema, 'name': 'user', 'sql': use, 'delimiter': '|'},
    {'schema': genre_schema, 'name': 'genre', 'sql': gen, 'delimiter': '|'},
    {'schema': item_schema, 'name': 'item', 'sql': ite, 'delimiter': '|'},
    {'schema': data_schema, 'name': 'data', 'sql': dat, 'delimiter': '\t'}
]



# create table and load data
for table_item in table_list:
    try:
        print('processing ' + str(table_item['name']))
        create_table(table_item['schema'], table_item['name'])
        load_data(table_item['sql'], 'u.' + table_item['name'], table_item['delimiter'])
        print('completed table creation and data load for ' + table_item['name'])
    except:
        print('****** error processing ' + str(table_item['name'] + '******'))
        continue

print('data inserted into tables')

# my advice on coding
# more logs to show status
# use one method for executemany 'DONOT REPEAT'

# my advice on table generation
# sql table using 'IF exist'
# adjust data if id is in the second column
# use foreign key to establish relationship

# 练习
# exercise: https://www.w3schools.com/sql/sql_exercises.asp
# go back to previous numpy exercise to adjust merge option compare difference
# 重新调整SCHEMA,重新执行PYTHON程序，将数据录入。

# query study:
# 1. 选DATA中最受欢迎（最多评论）的那一部电影，写出QUERY得到所有评分人名
# 2. 选出学生中最受欢迎的前五步电影。
# 3. 选出女性观众最不喜欢的3部电影
# 4. 选出年龄20-40岁之间观众最喜欢的爱情片
#1:
# a = 'with top_review as ' \
#     '(select item_id, count(item_id) as cnt ' \
#     'from data group by item_id order by cnt desc limit 1) ' \
#     'select user_id from data natural join top_review;'
# mycursor.execute(a)
# myresult1=mycursor.fetchall()


#2:
# b = 'with student_col as ' \
#     '(select * from user natural join data where occupation = "student"),' \
#     'top_review as ' \
#     '(select movie_title, item_id, count(item_id) as cnt ' \
#     'from student_col inner join item on student_col.item_id = item.movie_id group by item_id ' \
#     'order by cnt desc limit 5)' \
#     'select movie_title from top_review'
#
# mycursor.execute(b)
# myresult2=mycursor.fetchall()

#3:
# c = 'with female_col as ' \
#     '(select * from user natural join data where gender = "M"),' \
#     'top_review as ' \
#     '(select movie_title, item_id, count(item_id) as cnt ' \
#     'from female_col inner join item on female_col.item_id = item.movie_id group by item_id ' \
#     'order by cnt limit 3)' \
#     'select movie_title from top_review'
#
# mycursor.execute(c)
# myresult3=mycursor.fetchall()


#4:
# d = 'with age_col as '\
#     '(select * from user natural join data where age between 20 and 40),' \
#     'romance_col as ' \
#     '(select * from item where romance=1),' \
#     'top_review as ' \
#     '(select movie_title, item_id, count(item_id) as cnt ' \
#     'from age_col inner join romance_col on age_col.item_id = romance_col.movie_id group by item_id ' \
#     'order by cnt desc limit 1)' \
#     'select movie_title from top_review '\
#
# mycursor.execute(d)
# myresult4=mycursor.fetchall()
# print(myresult4)


# additional comments 7/19
# 1. meaningful method names and variable (dddd)
# 2. comments to organize steps
# 3. use debug mode to find issue
# 4. single quote













