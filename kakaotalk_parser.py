"""
Example:
    python kakaotalk_parser.py talk_log.txt > talk_stats.txt
    python kakaotalk_parser.py --src_encoding=cp949 talk_log.txt > talk_stats.txt
"""
import argparse
import re

parser = argparse.ArgumentParser(description='kakaotalk stat collect')
parser.add_argument('infile', type=str)
parser.add_argument('--src_encoding', default='utf-8')

date = re.compile('^\d+년 \d+월 \d+일 \w+요일$')
chat = re.compile('^\d+/\d+/\d+ \w+ \d+:\d+, .*')
inout = re.compile('^\d+/\d+/\d+ \w+ \d+:\d+: .*')

def print_stats(db):
    for k, v in sorted(db.items(), key=lambda item: item[1], reverse=True):
        print("%s, %d" % (k, v))
    print("===================\n")

def collect_stats(fp):
    title = None
    timestamp = None

    lineno = 0
    user = ''
    text = ''
    total_db = dict()
    daily_db = None
    for line in fp:
        lineno += 1
        if (daily_db is None and re.match(date, line) is None):
            # Parser Init [optional]
            # line 0: Title
            # line 1: Timestamp
            if (lineno == 0):
                title = line
            elif (lineno == 1):
                timestamp = line
            # skip all lines until a line satisfies the correct date format
            continue

        # Parse body
        if (re.match(date, line) is not None):
            if (daily_db is not None):
                # display current daily stats
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
    # Parser complete
    if (daily_db is None):
        print("daily_db is empty: Unexpected format? (parsed %d lines)" % lineno)
    else:
        # print last daily stats
        print_stats(daily_db)

        print("Summary", timestamp)
        print_stats(total_db)

if __name__ == '__main__':
    args = parser.parse_args()

    filepath = args.infile
    with open(filepath, 'r', encoding=args.src_encoding) as f:
        collect_stats(f)
