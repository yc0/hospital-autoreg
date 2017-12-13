import argparse
import re
import requests
import threading


def doTask(sess, headers, payload, args):
    if args.verbose >= 3:
        print(sess)
        print(headers)
        print(payload)
        print(args)

    # resp = sess.post('https://www.hospital.com', headers=headers ,data=payload)
    resp = sess.post(
        'https://www.hospital.com/check',
        headers=headers,
        data=payload)
    resp.encoding = 'big5'
    # result
    if args.verbose >= 1:
        print(resp.text)


parser = argparse.ArgumentParser(
    description='使用方式如下:e,g, python ar.py -i A1234567890 -s\
     外科 -mm 01 -dd 01 -dr 都凱傑')
parser.add_argument(
    '-v',
    '--verbose',
    action='count',
    default=0,
    help='verbose. number of v for differnet levels, e.g. -v or -vv')
parser.add_argument(
    '-w',
    '--week',
    dest='isWithinWeek',
    choices=[
        'true',
        'false'],
    default='false',
    help='reserve within a week(true) or\
     beyond two weeks(false) (default:false)')
parser.add_argument('-i', '--id', required=True,
                    help='(required)your identification')
parser.add_argument(
    '-s',
    '--section',
    required=True,
    help='(required)which section/department you want to reserve.\
     It can only be provided partial keyword, \
     and it would automatically match the first one it meets')
parser.add_argument(
    '-mm',
    '--month',
    required=True,
    help='(required)the month of your birthday, \
    it should be two digit, e.g. 01,02,03')
parser.add_argument(
    '-dd',
    '--date',
    required=True,
    help='(required)the date of your birthday, \
    it should be two digit, e.g. 07,08,12')
parser.add_argument(
    '-dr',
    '--doctor',
    required=True,
    help='(required)the doctor you want to make an appointment')

args = parser.parse_args()

if args.verbose >= 3:
    print(args.isWithinWeek)
    print(args.id)
    print(args.month)
    print(args.date)
    print(args.doctor)
    print(args.section)


session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Accept-Language': 'zh-TW,en-US;q=0.8,en;q=0.6,zh;q=0.4'}

resp = session.get(
    'https://www.hospital.com/op/htm',
    headers=headers)
resp.encoding = 'big5'

section = args.section
ID = args.id
birthday_m = args.month
birthday_d = args.date
isInTheTwoWeeks = args.isWithinWeek.lower() == 'true'
docter = args.doctor
section_id = None
reservation_id = None


mobj = re.search(
    r'<input type="radio" name="pdsect" value="([0-9a-zA-Z\-]*)">([^<]+)<',
    resp.text)
for m in re.finditer(
    r'<input type="radio" name="pdsect" value="([0-9a-zA-Z\-]*)">([^<]+)<[B|b]',
        resp.text):
    if re.search(r'' + section, m.group(2)):
        if args.verbose >= 1:
            print(m.group(1), m.group(2))
        section_id = m.group(1)
        break
if not section_id:
    raise Exception('沒有該專科，請試著調整您填寫的專科內容或確認後，再填寫')

payload = {
    'pdsect': section_id,
    'pg': 'Oregi01' if isInTheTwoWeeks else 'Oregi01d',
    'back': 'va.htm',
    'svl': 'Y'
}
headers = {
    'Referer': 'https://www.hospital.com/type_\
    ' + ('01' if isInTheTwoWeeks else '02'),
    'Origin': 'https://www.hospital.com',
    'Host': 'www.hospital.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Accept-Language': 'zh-TW,en-US;q=0.8,en;q=0.6,zh;q=0.4'
}
if args.verbose >= 1:
    print(payload)
if args.verbose >= 2:
    print(headers)
resp = session.post(
    "https://www.hospital.com/serv",
    data=payload)
resp.encoding = 'big5'
if args.verbose >= 2:
    print(resp.text)


for m in re.finditer(
    r'<td[^>]*BGCOLOR=[^>]*>[^<]*<a[^:]*:CreateWindow[^>]*>(?P<doctor>[^\s+]*)[^<]*[^i]*input type=radio name=oregkey value=(?P<val>[^\s]+)\s*[^>]*>',
        resp.text):
    if args.verbose >= 1:
        print(m.group('doctor'), m.group('val'))
    if re.search(r'' + docter, m.group('doctor')):
        if not reservation_id:
            reservation_id = [m.group('val')]
        else:
            reservation_id += [m.group('val')]
        if args.verbose >= 1:
            print(m.group('doctor'), m.group('val'))

if not reservation_id:
    raise Exception('沒有該醫生或該時段此醫生沒有診')


mobj = re.search(
    r'<input[^>]*type=hidden name=pg[^=]*=(?P<pg>[^>]*)',
    resp.text)
pg = mobj.group('pg')
mobj = re.search(
    r'<input[^>]*type=hidden name=svl[^=]*=(?P<svl>[^>]*)',
    resp.text)
svl = mobj.group('svl')

headers = {
    'Referer': 'https://www.hospital.com/type_\
    ' + '01' if isInTheTwoWeeks else '01d',
    'Origin': 'https://www.hospital.com',
    'Host': 'www.hospital.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Accept-Language': 'zh-TW,en-US;q=0.8,en;q=0.6,zh;q=0.4'}


for ri in reservation_id:
    payload = {
        'oregkey': ri,  # 組織代號
        'pid': ID,  # 身份證
        'pbirth_mm': birthday_m,
        'pbirth_dd': birthday_d,
        'pg': pg,
        'svl': svl,
        'pwd': ''
    }
    t = threading.Thread(target=doTask,
                         args=(session, headers, payload, args))
    t.start()
