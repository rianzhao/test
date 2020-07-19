# mysql installation tutorial : https://www.dev2qa.com/how-to-use-mysql-on-mac/

# **** (use if needed) **** python set to 3.7.3 in mac: https://opensource.com/article/19/5/python-3-default-mac

# Python mysql tutorial: https://www.w3schools.com/python/python_mysql_getstarted.asp

# TODO : design table schema, put resources/customer_rating_movies into 6 tables in local mysql database using python programming
import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="zra19980318",
  database="mydatabase"
)

mycursor=mydb.cursor()


mycursor.execute("CREATE TABLE IF NOT EXISTS occupation (occu_name VARCHAR(255) PRIMARY KEY)")
print("table occupation created")

mycursor.execute("create table if not exists user"
                 "(user_id INT AUTO_INCREMENT PRIMARY KEY, "
                 "age INT UNSIGNED,"
                 "gender VARCHAR(255),"
                 "occupation VARCHAR(255),"
                 "zip_code VARCHAR(255),"
                 "foreign key(occupation) references occupation(occu_name))")
print("table user created")

mycursor.execute("create table if not exists genre"
                 "(type VARCHAR(255),"
                 "id INT PRIMARY KEY)")
print("table genre created")

mycursor.execute("create table if not exists info"
                 "(num INT,"
                 "type VARCHAR(255) PRIMARY KEY)")
print("table info created")

mycursor.execute("create table if not exists item"
                 "(movie_id INT AUTO_INCREMENT PRIMARY KEY,"
                 "movie_title VARCHAR(255),"
                 "release_date VARCHAR(255),"
                 "video_release_date VARCHAR(255),"
                 "IMDB_URL VARCHAR(255),"
                 "unknown INT CHECK(unknown=1 or unknown=0),"
                 "action INT CHECK(action=1 or action=0),"
                 "adventure INT CHECK(adventure=1 or adventure=0),"
                 "animation INT CHECK(animation=1 or animation=0),"
                 "childrens INT CHECK(childrens=1 or childrens=0),"
                 "comedy INT CHECK(comedy=1 or comedy=0),"
                 "crime INT CHECK(crime=1 or crime=0),"
                 "documentary INT CHECK(documentary=1 or documentary=0),"
                 "drama INT CHECK(drama=1 or drama=0),"
                 "fantasy INT CHECK(fantasy=1 or fantasy=0),"
                 "film_noir INT CHECK(film_noir=1 or film_noir=0),"
                 "horror INT CHECK(horror=1 or horror=0),"
                 "musical INT CHECK(musical=1 or musical=0),"
                 "mystery INT CHECK(mystery=1 or mystery=0),"
                 "romance INT CHECK(romance=1 or romance=0),"
                 "sci_fi INT CHECK(sci_fi=1 or sci_fi=0),"
                 "thriller INT CHECK(thriller=1 or thriller=0),"
                 "war INT CHECK(war=1 or war=0),"
                 "western INT CHECK(western=1 or western=0))")
print("table item created")

mycursor.execute("create table if not exists ddddata"
                 "(user_id INT(11), "
                 "item_id INT(11), "
                 "rating INT(5) CHECK (rating >= 1 and rating <= 5),"
                 "timestamp VARCHAR(255),"
                 "PRIMARY KEY (user_id, item_id),"
                 "foreign key (user_id) references user(user_id),"
                 "foreign key (item_id) references item(movie_id))")
print("table data created")

occu="INSERT INTO occupation (occu_name) VALUE (%s)"

dat="INSERT INTO ddddata (user_id, item_id, rating, timestamp) VALUES (%s, %s, %s,%s)"

use="INSERT INTO user (user_id, age, gender, occupation, zip_code) VALUES (%s, %s, %s, %s, %s)"

gen="INSERT INTO genre (type, id) VALUES (%s, %s)"

info="INSERT INTO info (num, type) VALUES (%s, %s)"

ite="INSERT INTO item (movie_id, movie_title, release_date, video_release_date, " \
    "IMDB_URL, unknown, action, adventure, animation, childrens, comedy, crime, " \
    "documentary, drama, fantasy, film_noir, horror, musical, mystery, romance, sci_fi, thriller, war, western) " \
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"

prefix = "./resources/customers_rating_movies_data/"

def read_file(filename, delimiter=" ", col_name=True):
  res = []
  with open(filename) as fin:
    if col_name:
      next(fin)

    for line in fin:
      item = tuple(line.strip().split(delimiter))
      res.append(item)

  return res



# mycursor.executemany(occu, read_file(prefix + "u.occupation", col_name=False))
# mycursor.executemany(use, read_file(prefix + "u.user", delimiter="|"))
# mycursor.executemany(gen, read_file(prefix + "u.genre", delimiter="|", col_name=False))
# mycursor.executemany(info,read_file(prefix + "u.info", delimiter=" ", col_name=False))
# mycursor.executemany(ite, read_file(prefix + "u.item", delimiter="|"))
# mycursor.executemany(dat, read_file(prefix + "u.data", delimiter='\t'))

print("data inserted into tables")
mydb.commit()



# my advice on coding
# more logs to show status
# use one method for executemany "DONOT REPEAT"

# my advice on table generation
# sql table using "IF exist"
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
a = "with top_review as " \
    "(select item_id, count(item_id) as cnt " \
    "from ddddata group by item_id order by cnt desc limit 1) " \
    "select user_id from ddddata natural join top_review;"
mycursor.execute(a)
myresult1=mycursor.fetchall()


#2:
b = "with student_col as " \
    "(select * from user natural join ddddata where occupation = 'student')," \
    "top_review as " \
    "(select movie_title, item_id, count(item_id) as cnt " \
    "from student_col inner join item on student_col.item_id = item.movie_id group by item_id " \
    "order by cnt desc limit 5)" \
    "select movie_title from top_review"

mycursor.execute(b)
myresult2=mycursor.fetchall()

#3:
c = "with female_col as " \
    "(select * from user natural join ddddata where gender = 'M')," \
    "top_review as " \
    "(select movie_title, item_id, count(item_id) as cnt " \
    "from female_col inner join item on female_col.item_id = item.movie_id group by item_id " \
    "order by cnt limit 3)" \
    "select movie_title from top_review"

mycursor.execute(c)
myresult3=mycursor.fetchall()


#4:
d = "with age_col as "\
    "(select * from user natural join ddddata where age between 20 and 40)," \
    "romance_col as " \
    "(select * from item where romance=1)," \
    "top_review as " \
    "(select movie_title, item_id, count(item_id) as cnt " \
    "from age_col inner join romance_col on age_col.item_id = romance_col.movie_id group by item_id " \
    "order by cnt desc limit 1)" \
    "select movie_title from top_review "\

mycursor.execute(d)
myresult4=mycursor.fetchall()
print(myresult4)













