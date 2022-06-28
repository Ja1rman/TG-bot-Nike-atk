import telebot
import requests

bot = telebot.TeleBot('')

@bot.message_handler(content_types=['text'])
def getSend(message):
    mes = message.text
    if (mes.find(' ')) != -1: bot.send_message(message.from_user.id, stock(mes[:mes.find(' ')], int(mes[mes.find(' ')+1:])))
    else: bot.send_message(message.from_user.id, stock(mes))

def stock(url, formUrl=0):

    response = requests.get(url).text
    styleCode = response[response.find('styleColor" content="')+21:]
    styleCode = styleCode[:styleCode.find('"')]

    productId = response[response.find('productId" content="')+20:]
    productId = productId[:productId.find('"')]
    atk = url + '/?productId=' + productId + '&size='

    url = 'https://api.nike.com/merch/skus/v2/?filter=productId%28' + productId + '%29&filter=country%28RU%29'
    response = requests.get(url).json()['objects']
    sizes = []
    for size in response:
        sizes.append(size['nikeSize'])

    url = 'https://api.nike.com/deliver/available_gtins/v2/?filter=styleColor%28' + styleCode + '%29&filter=merchGroup%28XP%29'
    response = requests.get(url).json()['objects']
    stocks = []
    for stock in response:
        stocks.append(stock['level'])

    stockSize = {}
    for i in range(0, len(sizes)):
        stockSize[sizes[i]] = stocks[i]

    api_key = 'e99cf8bb-52dd-4602-963a-f15f09aa50f8'
    res = ''
    for key, value in stockSize.items():
        if formUrl:
            ATK = 'https://hm.ru/' + requests.post('https://api.hm.ru/key/url/shorten', 
                json={'api_key': api_key, 'url': atk + key}).json()['data']['short_code']
        else: ATK = atk + key
        res += key + ' - ' + value + ' ' + ATK + '\n'
    return res

if __name__ == '__main__':
    while True:
        try: bot.polling(none_stop=True, interval=0)
        except: pass
