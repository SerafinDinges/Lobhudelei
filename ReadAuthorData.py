import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from collections import Counter
import datetime

url = 'https://netzpolitik.org/author/chris-koever/page/'

filename = 'chris.csv'

with open(filename, 'w') as f:
    i = 1
    allText = ""
    while i < 9:
        r = requests.get(url + str(i))
        print(r)
        print(' (' + url + str(i) + ')')
        html_contents = r.text
        html_soup = BeautifulSoup(html_contents, features='html.parser')

        start_date = datetime.datetime.now() - datetime.timedelta(days=7)
        start_date = start_date.date()

        for teaser__link in html_soup.select('a.teaser__headline-link'):

            link = teaser__link['href']
            print("Getting words from " + link)

            html_page_contents = requests.get(link).text
            html_page_soup = BeautifulSoup(
                html_page_contents, features='html.parser')
            entry_content = html_page_soup.select_one('div.entry-content')
            # for paragraph in html_page_soup.select('p'):
            allText += entry_content.text

            # lines = link + '\n'
        i += 1

    whiteSpaceRegex = "\\s"
    # SANITISE TEXT
    allText = allText.replace(".", "")
    allText = allText.replace("!", "")
    allText = allText.replace("?", "")
    allText = allText.replace(";", "")
    # allText = allText.replace(":", "")
    allText = allText.replace("–", "")
    allText = allText.replace(",", "")
    allText = allText.replace("\"", "")
    allText = allText.replace("„", "")
    allText = allText.replace("“", "")
    allText = allText.replace("‚", "")
    allText = allText.replace("‘", "")
    allText = allText.replace("'", "")

    allWords = allText.split()
    wordcount = Counter(allWords)
    wordcount = wordcount.most_common()
    for word, count in wordcount:
        f.writelines(word + "," + str(count) + "\n")

print('Siehe {}'.format(filename))
