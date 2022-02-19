from cmd import Cmd
from controller import Controller

class Interface(Cmd):
  intro = 'Witaj! Wpisz help lub ?, aby zobaczyć dostępne komendy.\n'
  doc_header = 'Dostępne komendy (wpisz help <komenda>):'
  prompt = '> '

  def __init__(self, controller: Controller=None):
    super().__init__()
    self.controller = controller if controller else Controller()

  def do_add(self, arg):
    'Dodaj kurs do listy ukończonych kursów: add <nazwa kursu> <semestr: lato|zima> <rok: 2016/17|2017/18|...>'
    self.controller.add(arg)

  def do_rm(self, arg):
    'Usuń kurs z listy ukończonych kursów: rm <nazwa kursu> <semestr: lato|zima> <rok: 2016/17|2017/18|...>'
    self.controller.remove(arg)
  
  def do_ls(self, arg):
    'Wypisz wszystkie kursy z listy ukończonych kursów'
    self.controller.list()
  
  def do_calce(self, arg):
    'Oblicz, czego jeszcze brakuje ci do zaliczenia studiów inżynierskich'
    self.controller.calculate_engineer()

  def do_calcb(self, arg):
    'Oblicz, czego jeszcze brakuje ci do zaliczenia studiów licencjackich'
    self.controller.calculate_bachelor()
  
  def do_update(self, arg):
    'Uaktualnij bazę danych z kursami'
    self.controller.update()

  def do_q(self, arg):
    'Zamknij program'
    self.controller.quit()
  
  def do_save(self, arg):
    'Zapisz lokalnie listę ukończonych kursów'
    self.controller.save()

  def complete_add(self, text, line, begidx, endidx):
    return self.controller.complete_add(text, line)

  def complete_rm(self, text, line, begidx, endidx):
    return self.controller.complete_rm(text, line)

  def precmd(self, line):
    return line.lower()

  def default(self, line):
    self.controller.default(line)

  def emptyline(self):
    return