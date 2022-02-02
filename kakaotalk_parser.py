import argparse
import pprint
import re

parser = argparse.ArgumentParser(description='kakaotalk stat collect')
parser.add_argument('infile', type=str)

date = re.compile('^\d+년 \d+월 \d+일 \w+요일$')
chat = re.compile('^\d+/\d+/\d+ \w+ \d+:\d+, .*')
inout = re.compile('^\d+/\d+/\d+ \w+ \d+:\d+: .*')

def print_stats(db):
    for k, v in sorted(db.items(), key=lambda item: item[1], reverse=True):
        print("%s, %d" % (k, v))
    print("===================\n")

if __name__ == '__main__':
    args = parser.parse_args()

    filepath = args.infile

    title = None
    timestamp = None
    with open(filepath, 'r') as f:
        lineno = 0
        user = ''
        text = ''
        total_db = dict()
        daily_db = None
        for line in f:
            if (lineno == 0):
                title = line
            elif (lineno == 1):
                timestamp = line
            else:
                if (re.match(date, line) is not None):
                    if (daily_db is not None):
                        print_stats(daily_db)
                    # log start date
                    print(line)
                    daily_db = dict()
                elif (re.match(chat, line) is not None):
                    # end of prev text
                    # print(text)
                    if (len(user) > 0):
                        total_db[user] = total_db.get(user, 0) + 1
                        daily_db[user] = daily_db.get(user, 0) + 1
                    time, msg = re.split(',\s', line, maxsplit=1)
                    user, text = re.split(' : ', msg, maxsplit=1)
                elif (re.match(inout, line) is not None):
                    print(line.rstrip())
                else:
                    text = text + line

            lineno += 1
    print_stats(daily_db)

    print("Summary", timestamp)
    print_stats(total_db)
