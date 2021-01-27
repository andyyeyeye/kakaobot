import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import json
import os
class HTMLTableParser(HTMLParser):
    """ This class serves as a html table parser. It is able to parse multiple
    tables which you feed in. You can access the result per .tables field.
    """
    def __init__(
        self,
        decode_html_entities=False,
        data_separator=' ',
    ):

        HTMLParser.__init__(self, convert_charrefs=decode_html_entities)

        self._data_separator = data_separator

        self._in_td = False
        self._in_th = False
        self._current_table = []
        self._current_row = []
        self._current_cell = []
        self.tables = []

    def handle_starttag(self, tag, attrs):
        """ We need to remember the opening point for the content of interest.
        The other tags (<table>, <tr>) are only handled at the closing point.
        """
        if tag == 'td':
            self._in_td = True
        if tag == 'th':
            self._in_th = True

    def handle_data(self, data):
        """ This is where we save content to a cell """
        if self._in_td or self._in_th:
            self._current_cell.append(data.strip())

    def handle_endtag(self, tag):
        """ Here we exit the tags. If the closing tag is </tr>, we know that we
        can save our currently parsed cells to the current table as a row and
        prepare for a new row. If the closing tag is </table>, we save the
        current table and prepare for a new one.
        """
        if tag == 'td':
            self._in_td = False
        elif tag == 'th':
            self._in_th = False

        if tag in ['td', 'th']:
            final_cell = self._data_separator.join(self._current_cell).strip()
            self._current_row.append(final_cell)
            self._current_cell = []
        elif tag == 'tr':
            self._current_table.append(self._current_row)
            self._current_row = []
        elif tag == 'table':
            self.tables.append(self._current_table)
            self._current_table = []

def get_food():

    response = requests.get('https://www.ksa.hs.kr/Home/CafeteriaMenu/72')

    soup = BeautifulSoup(response.text,'html.parser')
    table = soup.find_all('table',{'class':'table table-bordered meal'})
    p = HTMLTableParser()
    p.feed(str(table))

    table = p.tables

    table = table[0]

    dic={}

    for i in range(1,len(table)):
        for j in range(0,len(table[1])):
            dic[table[0][j]]=table[i][j].replace("\n","  ")

    return dic

def learn(input):

    my_dir = os.path.dirname(__file__)

    path = os.path.join(my_dir, 'learn.json')

    with open(path) as json_file:
        data = json.load(json_file)
        key = data.keys()

        if input['q'] in key:
            return False

        else:
            with open(path, 'w') as outfile:
                data[input['q']]=input['a']
                json.dump(data, outfile)
                return True

def say(input):

    my_dir = os.path.dirname(__file__)

    path = os.path.join(my_dir, 'learn.json')

    with open(path) as json_file:
        data = json.load(json_file)
        key = data.keys()

        if input in key:
            return data[input]
        else:
            return False


def chatbot(room, msg, sender, isGroupChat):
    if msg=="$test":
        return "room : "+room+", msg : "+msg+", sender : "+sender

    elif msg=="$급식" or msg=="$밥" or msg=="$ㅂ":
        try:
            bab = get_food()
            return "아침 : " + bab['아침']+'\n'+"점심 : " + bab['점심']+'\n'+"저녁 : " + bab['저녁']
        except:
            return "몰라여"

    elif msg=="$가르치기":
        return "저를 가르치기 위해서는 $가르치기@질문@대답 형식으로 알려주세요"
    elif '@' in msg:
        if msg.split('@')[0]=="$가르치기":
            if learn({'q':msg.split('@')[1],'a':msg.split('@')[2]}):
                return "성공!"
            else:
                return "벌써 배웠던 질문입니다"

    elif say(msg[1:]) != False:
        return say(msg[1:])

    else:
        return "아직 배우지 못한 명령입니다ㅜㅠ"
