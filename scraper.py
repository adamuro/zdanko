import json
import random
from threading import Thread
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

BASE_URL = 'https://zapisy.ii.uni.wroc.pl/courses'

class Scraper():
  def __init__(self, base_url):
    self.waiting_phrases = ['Momencik...', 'Chwilunia...', 'Już kończę...', 'Już prawie...', 'Jeszcze tylko...', 'Już blisko...', 'Ostatnia prosta...', 'Poczekaj...', 'Zaraz, zaraz...', 'Sekundka...', 'Yyy...', 'Teraz naprawdę...']
    self.base_url = base_url
    self.courses = []
    print('Pobieram kursy...')
    self.__scrap_courses()
    print('Mamy to!\n')

  def __soup(self, url):
    response = urlopen(url)
    html_decoded = response.read().decode('utf8')
    return bs(html_decoded, features='html.parser')

  def __courses_urls(self):
    links = self.__soup(self.base_url).find_all('a', { 'class': 'dropdown-item' })
    return [self.base_url + link.get('href').replace('/courses', '') for link in links]

  def __scrap_course(self, course):
    soup = self.__soup(self.base_url + course['url'].replace('/courses', ''))
    info = soup.find_all('td')

    term = soup.find('small', { 'class': 'text-muted' }).text
    name = course['name'].lower() + ' ' + term
    type = info[3].text.strip().replace('\n', '').lower()
    ects = int(info[4].text.strip().replace('\n', ''))
    effects = [effect.text.lower() for effect in soup.find_all('span', { 'class': 'badge badge-info mr-2' })]

    self.courses.append({
      'name': name,
      'type': type,
      'ects': ects,
      'effects': effects
    })

  def __scrap_courses(self):
    for url in self.__courses_urls():
      print(random.choice(self.waiting_phrases))

      threads = []
      courses_string = self.__soup(url).find('script', { 'id': 'courses-data' }).text

      for course in json.loads(courses_string):
        threads.append(Thread(target=self.__scrap_course, args=(course,)))
      for thread in threads:
        thread.start()
      for thread in threads:
        thread.join()

