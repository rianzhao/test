# 这是一些关于PYTHON编程的联系，你可以直接在题目后面写出代码。

# 1. 找出下面两个数组的公共部分并打印出来
#   a = [1, 1, 2, 3, 5, 8, 15, 21, 34, 56, 86]
#   b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
#


def finding_commons(a, b):
    c = []
    for item in a:
        if (item in b) & (item not in c):
            c.append(item)
    print(c)


a = [1, 1, 2, 3, 5, 8, 15, 21, 34, 56, 86]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
finding_commons(a, b)
#
# 2. 将数组里重复的数字除去。打印出最后结果。
#   list = [1, 1, 1, 2, 3, 3, 3, 3, 4, 5, 6, 7, 7, 8, 9, 9, 10, 11, 12, 12, 13, 14]
#


def remove_duplicate(a):
    b = []
    for item in a:
        if item not in b:
            b.append(item)
    print(b)


list = [1, 1, 1, 2, 3, 3, 3, 3, 4, 5, 6, 7, 7, 8, 9, 9, 10, 11, 12, 12, 13, 14]
remove_duplicate(list)
#
# 3. 统计下面的数列，用MAP格式打印出各个水果有几个。
#   fruit = [apple, pear, mango, banana, banana, pear, apple, mango, banana]
#


def show_map(list):
    result = {}
    for item in list:
        if item not in result.keys():
            result[item] = 1
        else:
            result[item] += 1
    print(result)
    return result


fruit = ['apple', 'pear', 'mango', 'banana', 'banana', 'pear', 'apple', 'mango', 'banana']
show_map(fruit)

#

# 4. 在test项目目录中打开一个名为test.txt的文件，在已有文字后面，写入"hello world"。如果找不到文件，本地创建一个同名新文件。
#

# import os
# def add_to_file():
#     file_name = 'test.txt'
#     if not path.exists(file_name):
#         print('file not exist')
#         with open(file_name, 'w') as fp:
#             fp.write('hello world')
#             fp.close()
#     else:
#         f = open(file_name, 'r')
#         f.write('hello world')
#         f.close()


# add_to_file()


#
# 5. 用户指定一个数列，可以将1-10内数字英文单词变换成相应数字， 例如 [one, three, two, five, six] -> [1, 3, 2, 5, 6]
#

def map_to_number(list):
    number_dic = {'one':1, 'two': 2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10}
    result = []
    for item in list:
        result.append(number_dic[item])
    print(result)


number_list = ['one', 'three', 'two', 'five', 'six']
map_to_number(number_list)

#
# 6. 将给定数组里的数，分成奇数和偶数两个数列，分别打印出来。例如 [1,3,4,5,7,8,9,11,20] -> [1,3,5,7,9,11] [4,8,20]
#
#
def print_odd_even(list):
    odd_list = []
    even_list = []
    for i in list:
        if i%2 == 0:
            even_list.append(i)
        else:
            odd_list.append(i)
    print(odd_list)
    print(even_list)


n_list = [1,3,4,5,7,8,9,11,20]
print_odd_even(n_list)

# 7. 给定一段话，找出最高频的那个单词。例子中的 music.
# text = 'I mean, think about music. Music is all about repetition and patterns. If you didn’t have repetition in music, it would all just be noise.'
#


def get_most_often_word(p):
    content_list = p.lower().replace('.','').replace(',', '').split(' ')
    word_frequency = show_map(content_list)
    word_most_frequent = content_list[0]
    word_count = word_frequency[content_list[0]]
    for i in word_frequency.keys():
        if word_frequency[i] > word_count:
            word_most_frequent = i
            word_count = word_frequency[word_most_frequent]
    print('most frequent word is ' + word_most_frequent + ' with count ' + str(word_count))


text = 'I mean, think about music. Music is all about repetition and patterns. If you didn’t have repetition in music, it would all just be noise.'
get_most_often_word(text)


#
# 8. 按照数字大小顺序排列 ["1","11","3","22","32","4","2","201"]

def order_str(number_str):
    list1 = [int(x) for x in number_str]
    list1.sort()
    print([str(i) for i in list1])


a = ["1","11","3","22","32","4","2","201"]
order_str(a)
