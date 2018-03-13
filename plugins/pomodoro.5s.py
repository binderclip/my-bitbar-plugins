#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
# <bitbar.title>Pomodoro</bitbar.title>
# <bitbar.version>1.0</bitbar.version>
# <bitbar.author>clip</bitbar.author>
# <bitbar.author.github>binderclip</bitbar.author.github>
# <bitbar.desc>A simple pomodoro</bitbar.desc>
# <bitbar.dependencies>python3</bitbar.dependencies>
import argparse
import json
import math
import os
import time
from subprocess import call


POMO_M = 40     # default 40m


def get_status_file():
    home = os.path.expanduser("~")
    status_file = os.path.join(home, '.bitbar_pomodoro')
    return status_file


def get_file_path():
    return os.path.realpath(__file__)


def get_file_name():
    return os.path.basename(__file__)


def make_a_refresh():
    s = f"bitbar://refreshPlugin?name={get_file_name()}"
    call(['open', s])


def print_submenu():
    file_path = get_file_path()
    print('---')
    print(f'Start | bash="{file_path}" param1="-s"  terminal=false')
    print('X Start')
    for X in [10, 15, 20, 25, 30, 35]:
        print(f'-- {X} | bash="{file_path}" param1="-X {X}"  terminal=false')
    print(f'Stop | bash="{file_path}" param1="-x"  terminal=false')


def set_config(d):
    status_file = get_status_file()
    with open(status_file, 'w') as f:
        json.dump(d, f)


def read_config():
    status_file = get_status_file()
    try:
        with open(status_file) as f:
            try:
                config = json.load(f)
            except json.decoder.JSONDecodeError:
                config = {}
    except FileNotFoundError:
        config = {}
    return config


def set_start_time_to_now():
    set_config({'start_time': int(time.time())})


def set_start_time_to_x(X):
    now = int(time.time())
    start_time = now + (X - POMO_M) * 60
    set_config({'start_time': start_time})


def clear_start_time():
    set_config({'start_time': 0})


def make_notify():
    # set to your own notification func
    call(['/Users/clip/script/big', '🤣'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", action="store_true", help='Start')
    parser.add_argument("-X", "--x_start", type=int, help='Start with X minutes')
    parser.add_argument("-x", "--stop", action="store_true", help='Stop')
    args = parser.parse_args()

    if args.start:
        set_start_time_to_now()
        make_a_refresh()
    elif args.x_start:
        set_start_time_to_x(args.x_start)
        make_a_refresh()
    elif args.stop:
        clear_start_time()
        make_a_refresh()

    config = read_config()
    start_time = config.get('start_time', 0)
    now = int(time.time())
    m = math.ceil((start_time + POMO_M * 60 - now) / 60.0)
    if 0 < m:
        print(f'== {m} ==')
    elif m == 0:
        print('🍅')
        make_notify()
        clear_start_time()
    else:
        print('🍅')
    print_submenu()


if __name__ == '__main__':
    main()
