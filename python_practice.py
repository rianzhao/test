# 这是一些关于PYTHON编程的联系，你可以直接在题目后面写出代码。
import string
# 1. 找出下面两个数组的公共部分并打印出来
a = [1, 1, 2, 3, 5, 8, 15, 21, 34, 56, 86]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
c=list()
for i in range(len(a)):
    for j in range(len(b)):
        if a[i]==b[j] and a[i] not in c:
            c.append(a[i])
print(c)
#
# 2. 将数组里重复的数字除去。打印出最后结果。
list1 = [1, 1, 1, 2, 3, 3, 3, 3, 4, 5, 6, 7, 7, 8, 9, 9, 10, 11, 12, 12, 13, 14]
a=list()
for i in range(len(list1)):
    if list1[i] not in a:
        a.append(list1[i])
print(a)


#
# 3. 统计下面的数列，用MAP格式打印出各个水果有几个。
fruit = ['apple', 'pear', 'mango', 'banana', 'banana', 'pear', 'apple', 'mango', 'banana']
a={}
for i in fruit:
    a[i]=fruit.count(i)
print(a)
#
# 4. 在test项目目录中打开一个名为test.txt的文件，在已有文字后面，写入"hello world"。如果找不到文件，本地创建一个同名新文件。
f=open("test.txt","a")
f.write("hello world")
f.close()
#
# 5. 用户指定一个数列，可以将1-10内数字英文单词变换成相应数字， 例如 [one, three, two, five, six] -> [1, 3, 2, 5, 6]
def switch(l):
    a={'one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9','ten':'10'}
    b=list()
    for i in l:
        if i in a:
            i=a.setdefault(i)
        b.append(i)
    print(b)
a=['one','three','2','two','five','six','eleven']
switch(a)
# 6. 将给定数组里的数，分成奇数和偶数两个数列，分别打印出来。例如 [1,3,4,5,7,8,9,11,20] -> [1,3,5,7,9,11] [4,8,20]
a=[1,3,4,5,7,8,9,11,20]
def divide(l):
    a=list()
    b=list()
    for i in l:
        if i%2==0:
            b.append(i)
        else:
            a.append(i)
    print(a)
    print(b)
divide(a)
#
# 7. 给定一段话，找出最高频的那个单词。例子中的 music.
text = 'I mean, think about music. Music is all about repetition and patterns. If you didn’t have repetition in music, it would all just be noise.'
def findmax(l):
    a={}
    l=l.lower()
    for i in string.punctuation:
        l=l.replace(i,' ')
    l=l.split()
    for n in l:
        a[n]=l.count(n)
    b=max(a.values())
    for k, v in a.items():
        if v==b:
            print(k)
findmax(text)

# 8. 按照数字大小顺序排列 ["1","11","3","22","32","4","2","201"]
a=["1","11","3","22","32","4","2","201"]
def sort(l):
    a=list()
    for i in l:
        a.append(int(i))
    a.sort()
    print(a)
sort(a)

findmax('1,1,1,2,2,2,3,3,3')
