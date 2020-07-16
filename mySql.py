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

mycursor.execute("CREATE TABLE occupation (name VARCHAR(255))")
mycursor.execute("create table ddddata "
                 "(user_id INT(11), "
                 "item_id INT(11), "
                 "rating INT(5) CHECK (rating >= 1 and rating <= 5),"
                 "timestamp VARCHAR(255))")
mycursor.execute("create table user"
                 "(user_id INT AUTO_INCREMENT PRIMARY KEY, "
                 "age INT UNSIGNED,"
                 "gender VARCHAR(255),"
                 "occupation VARCHAR(255),"
                 "zip_code VARCHAR(255))")
mycursor.execute("create table genre"
                 "(type VARCHAR(255),"
                 "id INT PRIMARY KEY)")
mycursor.execute("create table info"
                 "(num INT,"
                 "type VARCHAR(255))")
mycursor.execute("create table item"
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

occu="INSERT INTO occupation (name) VALUE (%s)"

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

mycursor.executemany(occu, read_file(prefix + "u.occupation", col_name=False))
mycursor.executemany(dat, read_file(prefix + "u.data", delimiter='\t'))
mycursor.executemany(use, read_file(prefix + "u.user", delimiter="|"))
mycursor.executemany(gen, read_file(prefix + "u.genre", delimiter="|", col_name=False))
mycursor.executemany(info,read_file(prefix + "u.info", delimiter=" ", col_name=False))
mycursor.executemany(ite, read_file(prefix + "u.item", delimiter="|"))

mycursor.executemany(gen, [('unknown', '0'), ('Adventure', '2'), ('Animation', '3'), ("Children's", '4'), ('Comedy', '5'), ('Crime', '6'), ('Documentary', '7'), ('Drama', '8') ])

mydb.commit()










