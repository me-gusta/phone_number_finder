import re
from pathlib import Path
from string import ascii_letters
import argparse

import requests

FOLDER = Path(__file__).parent / 'downloads'
FOLDER.mkdir(exist_ok=True)
regex = re.compile(r'^((8|\+7)[\- ]?)(\(?\d{3}\)?[\- ]?)[\d\- ]{7,10}$')

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, help='path to the input file')
parser.add_argument('--script', type=str, help='which script to run: "download" | "find" | "both"')


def make_file_stem(string: str):
    def validate_char(c: str):
        return c in ascii_letters

    return ''.join([x for x in string if validate_char(x)]).lower()


def write_file(name: str, content: str):
    with open(FOLDER / name, 'w+', encoding='utf-8') as f:
        f.write(content)


def download_html_page(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        print(f'unable to download {url=}')
        print(f'{response.status_code=}')
        return
    file_name = make_file_stem(
        url.removeprefix('https')
    ) + '.html'
    write_file(file_name, response.text)
    print(f'success {url}')


def find_numbers(string: str):
    def get_chat(c: str):
        if c.isdigit() or c in '+-() \n':
            return c
        return '\n'

    t = ''.join([get_chat(x) for x in string])
    matches = set()
    for line in t.splitlines():
        if match := regex.match(line.strip()):
            result = match.string
            only_digits = [x for x in result if x.isdigit()]
            if len(only_digits) == 11:
                matches.add(result)
    return list(matches)


def run_find():
    for path in FOLDER.iterdir():
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f'searching for urls in {str(path)}')
        result = find_numbers(text)
        print(f'{result=}\n')


def run_download(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    urls = text.splitlines()
    for url in urls:
        download_html_page(url)


def main():
    args = parser.parse_args()
    script = args.script
    if script in ['both', 'download']:
        file_path = Path(args.file)
        run_download(file_path)
        print('script "download" finished\n')
    if script in ['both', 'find']:
        run_find()
        print('script "find" finished\n')


if __name__ == '__main__':
    main()
