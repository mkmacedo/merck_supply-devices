from datetime import datetime

from pandas import read_excel

dateString = '01/05/2022'
x = datetime.strptime(dateString, '%d/%m/%Y')
y = x.strftime('%b %Y').upper()

print(type(x))

print(y)
print(type(y))

x = [1,2,3,4,5]

print(x[2:5])

for i in range(len(x)):
    if type(x[i]) == type(1):
        print(i)


df = read_excel('forecast_device.xlsx')

print(df.head(4))
