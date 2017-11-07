import os

Username = 'QY'
PassWord = '123456'

data = open('./Users/Users.txt', 'a')
str = Username + ':' + PassWord + '\n'
data.write(str)
data.close()
