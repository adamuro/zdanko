from cmd import Cmd
from courses import CoursesList, CoursesRepository
from requirements import Requirements

class Interface(Cmd):
  intro = 'Witaj! Wpisz help lub ?, aby zobaczyć dostępne komendy.\n'
  doc_header = 'Dostępne komendy (wpisz help <komenda>):'
  prompt = '> '

  def __init__(self, requirements: Requirements, finished_courses: CoursesList=CoursesList(), repository: CoursesRepository=CoursesRepository()):
    super().__init__()
    self.requirements = requirements
    self.finished_courses = finished_courses
    self.repository = repository
    self.courses = CoursesList(repository.find_all()) # Because reading courses directly from the repository every time is too slow

  def do_add(self, arg):
    'Dodaj kurs do listy ukończonych kursów: add <nazwa kursu> <semestr: lato|zima> <rok: 2016/17|2017/18|...>'
    course = self.courses.name(arg)
    if not course:
      print('Nie znaleziono kursu o nazwie "' + arg + '". Spróbuj skorzystać z auto-uzupełniania pod tabem :^)')
    else:
      self.finished_courses.add(course)
      print('Kurs o nazwie "' + arg + '" został dodany do listy!')

  def do_rm(self, arg):
    'Usuń kurs z listy ukończonych kursów: rm <nazwa kursu> <semestr: lato|zima> <rok: 2016/17|2017/18|...>'
    course = self.finished_courses.name(arg)
    if not course:
      print('Nie znaleziono kursu o nazwie "' + arg + '" na liście ukończonych kursów.\nSpróbuj skorzystać z auto-uzupełniania pod tabem :^)')
    else:
      self.finished_courses.remove(course)
      print('Kurs o nazwie "' + arg + '" został usunięty z listy!')
  
  def do_ls(self, arg):
    'Wypisz wszystkie kursy z listy ukończonych kursów'
    print(self.finished_courses.names())
  
  def do_calc(self, arg):
    'Oblicz, czego jeszcze brakuje ci do osiągnięcia wymaganych efektów kształcenia'
    types_lacks, effects_lacks = self.requirements.check_engineer(self.finished_courses.all())
    print(types_lacks)
    print(effects_lacks)
  
  def do_update(self, arg):
    'Uaktualnij bazę danych z kursami'
    if self.repository.update():
      self.courses = self.repository.find_all()

  def do_q(self, arg):
    'Zamknij program'
    print('Do zobaczenia!')
    exit()

  def complete_add(self, text, line, begidx, endidx):
    # Cmd autocompletes only the last word so we need to skip all the words before (offset)
    arg = line.partition(' ')[2]
    offset = len(arg) - len(text)
    return [name[offset:] for name in self.courses.names() if name.startswith(arg)]

  def complete_rm(self, text, line, begidx, endidx):
    # Cmd autocompletes only the last word so we need to skip all the words before (offset)
    arg = line.partition(' ')[2]
    offset = len(arg) - len(text)
    return [name[offset:] for name in self.finished_courses.names() if name.startswith(arg)]

  def precmd(self, line):
    return line.lower()

  def emptyline(self):
    return

Interface(Requirements()).cmdloop()