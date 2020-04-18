import requests
from bs4 import BeautifulSoup
import wget
import urllib.request
import sys
import json

if (sys.version_info > (3, 0)):
    pass
else:
    print("Python 3 required!")
    exit(0)


class Scraper(object):

    def __init__(self):
        self.api_counter = 1

    def download(self, url):
        try:
            print(url)
            wget.download(url)
        except:
            f = open("exceptions.txt", "a+")
            f.write(url + '\n')
            f.close()

    def scrapeAPI(self, id):

        json_data = urllib.request.urlopen(
            'https://podbay.fm/api/episodes?podcastID=' + str(id) + '&page=' + str(self.api_counter))
        j = json.loads(json_data.read())
        if (len(j['episodes']) > 0):
            for a in j['episodes']:
                self.download(a['enclosure']['url'])
            self.api_counter += 1
            self.scrapeAPI(id)

        else:
            print('Finished downloads')
            exit(0)

    def scrape(self, target_url):

        id = target_url.rsplit('/', 1)[-1]

        page = requests.get(target_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        episodes = soup.find(class_='episode-list')
        podcasts = episodes.find_all(class_="preview")
        for pod in podcasts:
            url = pod.find(rel="nofollow")['href']
            self.download(url)
        self.scrapeAPI(id)


if __name__ == "__main__":
    scraper = Scraper()

    scraper.scrape(sys.argv[1])
