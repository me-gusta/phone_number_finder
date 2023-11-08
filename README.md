# Phone Number Finder

With this script you can
1. Download an html page at specified urls
2. Find phone numbers in those pages

requirements:
- requests

Download files to the `/dowloads` folder.
Input file must contain urls separated by line break.
```
python main.py --script download --file PATH_TO_FILE
```


Go through files in `/downloads` and extract phone numbers.
```
python main.py --script find
```


Do both
```
python main.py --script both -- file PATH_TO_FILE
```
