# from pprint import pprint
#
# import requests
#
# # spu = 'https://dw4.co/t/A/1Gzc1gsi'
# spu = '2444035'
# r = requests.get('http://194.58.109.219:8000/api/v3/get_product/',
#                  params={
#                      'apikey': '10eWMOGJ0CbclthTww94NJliujh8G2g6',
#                      'spu': spu
#                  })
# pprint(r.json())
from Translator import Translator

t = Translator()
print(t.translate('1964年1月，当时身为俄勒冈州大学（University of Oregon）田径运动员的菲尔·奈特 （Phil Knight）和他的教练比尔·鲍尔曼（Bill Bowerman）创建了耐克（NIKE）的前身：“蓝丝带体育”（Blue Ribbon Sports）公司。1972年，2位创始人决定开发并制造自主设计的鞋，并给这种鞋取名耐克（NIKE），这是依照希腊胜利之神（Greek goddess of victory）的名字而取。'))