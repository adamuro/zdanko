import cmd
from scraper import Scraper

def add(course):
  print(course)

BASE_URL = 'https://zapisy.ii.uni.wroc.pl/courses'
courses = Scraper(BASE_URL).courses

class Interface(cmd.Cmd):
  intro = 'Witaj! Wpisz ? lub help, aby zobaczyć dostępne komendy.\n'
  prompt = '> '

  def do_add(self, arg):
    'Dodaj kurs do swojej listy ukończonych kursów: add <nazwa kursu> <semestr: lato|zima> <rok: 2016/17|2017/18|...>'
    add(arg)

  def complete_add(self, text, line, begidx, endidx):
    # Cmd autocompletes only the last word so we need to skip all the words before (offset)
    arg = line.partition(' ')[2]
    offset = len(arg) - len(text)
    completions = [c['name'][offset:] for c in courses if c['name'].startswith(arg)]
    
    
    return completions

  def precmd(self, line):
    return line.lower()

Interface().cmdloop()