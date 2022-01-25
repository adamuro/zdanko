import sys
from cmd import Cmd
from courses import CoursesList, CoursesRepository
from requirements import Requirements

class Interface(Cmd):
  intro = 'Witaj! Wpisz help lub ?, aby zobaczyć dostępne komendy.\n'
  doc_header = 'Dostępne komendy (wpisz help <komenda>):'
  prompt = '> '

  def __init__(self, requirements: Requirements=Requirements(), finished_courses: CoursesList=CoursesList(), repository: CoursesRepository=CoursesRepository()):
    super().__init__()
    self.requirements = requirements
    self.finished_courses = finished_courses
    self.repository = repository
    self.courses = CoursesList(repository.find_all()) # Because reading courses directly from the repository every time is too slow

  def do_add(self, arg):
    'Dodaj kurs do listy ukończonych kursów: add <nazwa kursu> <semestr: lato|zima> <rok: 2016/17|2017/18|...>'
    course = self.courses.name(arg)
    if not course:
      self.stdout.write(f'Nie znaleziono kursu o nazwie "{arg}". Spróbuj skorzystać z auto-uzupełniania pod tabem :^)\n')
    else:
      self.finished_courses.add(course)
      self.stdout.write(f'Kurs o nazwie "{arg}" został dodany do listy!\n')

  def do_rm(self, arg):
    'Usuń kurs z listy ukończonych kursów: rm <nazwa kursu> <semestr: lato|zima> <rok: 2016/17|2017/18|...>'
    course = self.finished_courses.name(arg)
    if not course:
      self.stdout.write(f'Nie znaleziono kursu o nazwie "{arg}" na liście ukończonych kursów.\nSpróbuj skorzystać z auto-uzupełniania pod tabem :^)\n')
    else:
      self.finished_courses.remove(course)
      self.stdout.write(f'Kurs o nazwie "{arg}" został usunięty z listy!\n')
  
  def do_ls(self, arg):
    'Wypisz wszystkie kursy z listy ukończonych kursów'
    if self.finished_courses.empty():
      self.stdout.write('Brak ukończonych kursów na liście\n')
    for name in self.finished_courses.names():
      self.stdout.write(f'{name}\n')
  
  def do_calc(self, arg):
    'Oblicz, czego jeszcze brakuje ci do osiągnięcia wymaganych efektów kształcenia'
    types_lacks, effects_lacks = self.requirements.check_engineer(self.finished_courses.all())
    if types_lacks:
      self.stdout.write('\n*** Liczba ECTS potrzebna do uzyskania z przedmiotów o typie z danej grupy: ***\n')
    for lack in types_lacks:
      types = lack['types']
      ects = lack['ects']
      self.stdout.write('- ')
      for i, type in enumerate(types, start=1):
        self.stdout.write(f'{type}: {ects}\n' if i == len(types) else f'{type}, ')
    if effects_lacks:
      self.stdout.write('\n*** Efekty kształcenia potrzebne do zaliczenia: ***\n')
    for effect in effects_lacks:
      self.stdout.write(f'- {effect}\n')
  
  def do_update(self, arg):
    'Uaktualnij bazę danych z kursami'
    if self.repository.update():
      self.courses = self.repository.find_all()

  def do_q(self, arg):
    'Zamknij program'
    self.stdout.write('Do zobaczenia!\n')
    sys.exit()

  def complete_add(self, text, line, begidx, endidx):
    return self.courses.completions(text, line)

  def complete_rm(self, text, line, begidx, endidx):
    return self.finished_courses.completions(text, line)

  def precmd(self, line):
    return line.lower()

  def default(self, line):
    command = line.partition(' ')[0]
    self.stdout.write(f'Niepoprawna komenda: "{command}".\nWpisz help lub ?, aby zobaczyć dostępne komendy.\n')

  def emptyline(self):
    return