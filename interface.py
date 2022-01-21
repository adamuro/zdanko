import cmd

from scraper import Scraper
from requirements import Requirements

BASE_URL = 'https://zapisy.ii.uni.wroc.pl/courses'
courses = Scraper(BASE_URL).courses
requirements = Requirements()

class Interface(cmd.Cmd):
  intro = 'Witaj! Wpisz ? lub help, aby zobaczyć dostępne komendy.\n'
  prompt = '> '

  def do_add(self, arg):
    'Dodaj kurs do listy ukończonych kursów: add <nazwa kursu> <semestr: lato|zima> <rok: 2016/17|2017/18|...>'
    matches = [course for course in courses if course['name'] == arg]
    if len(matches) == 0:
      print('Nie znaleziono kursu o nazwie "' + arg + '". Spróbuj skorzystać z auto-uzupełniania pod tabem :^)')
    else:
      requirements.add_course(matches[0])
      print('Kurs o nazwie "' + arg + '" został dodany do listy!')

  def do_rm(self, arg):
    'Usuń kurs z listy ukończonych kursów: rm <nazwa kursu> <semestr: lato|zima> <rok: 2016/17|2017/18|...>'
    matches = [course for course in requirements.courses if course['name'] == arg]
    if len(matches) == 0:
      print('Nie znaleziono kursu o nazwie "' + arg + '" na liście ukończonych kursów.\nSpróbuj skorzystać z auto-uzupełniania pod tabem :^)')
    else:
      requirements.remove_course(matches[0])
      print('Kurs o nazwie "' + arg + '" został usunięty z listy!')
  
  def do_ls(self, arg):
    'Wypisz wszystkie kursy z listy ukończonych kursów'
    print([course['name'] for course in requirements.courses])
  
  def do_calc(self, arg):
    'Oblicz, czego jeszcze brakuje ci do osiągnięcia wymaganych efektów kształcenia'
    print(requirements.check_engineer()['types'])
    print(requirements.check_engineer()['effects'])

  def do_q(self, arg):
    print('Do zobaczenia!')
    exit()

  def complete_add(self, text, line, begidx, endidx):
    # Cmd autocompletes only the last word so we need to skip all the words before (offset)
    arg = line.partition(' ')[2]
    offset = len(arg) - len(text)
    return [c['name'][offset:] for c in courses if c['name'].startswith(arg)]

  def complete_rm(self, text, line, begidx, endidx):
    # Cmd autocompletes only the last word so we need to skip all the words before (offset)
    arg = line.partition(' ')[2]
    offset = len(arg) - len(text)
    return [c['name'][offset:] for c in requirements.courses if c['name'].startswith(arg)]

  def precmd(self, line):
    return line.lower()

Interface().cmdloop()