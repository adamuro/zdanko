import sys
from courses import CoursesList, CoursesRepository
from requirements import Requirements

class Controller:
  def __init__(self, requirements: Requirements=Requirements(), finished_courses: CoursesList=CoursesList(), repository: CoursesRepository=CoursesRepository()):
    self.requirements = requirements
    self.finished_courses = finished_courses
    self.repository = repository
    self.courses = CoursesList(repository.find_all()) # Because reading courses directly from the repository every time is too slow

  def add(self, arg):
    course = self.courses.name(arg)
    if not course:
      sys.stdout.write(f'Nie znaleziono kursu o nazwie "{arg}". Spróbuj skorzystać z auto-uzupełniania pod tabem :^)\n')
    else:
      self.finished_courses.add(course)
      sys.stdout.write(f'Kurs o nazwie "{arg}" został dodany do listy!\n')

  def remove(self, arg):
    course = self.finished_courses.name(arg)
    if not course:
      sys.stdout.write(f'Nie znaleziono kursu o nazwie "{arg}" na liście ukończonych kursów.\nSpróbuj skorzystać z auto-uzupełniania pod tabem :^)\n')
    else:
      self.finished_courses.remove(course)
      sys.stdout.write(f'Kurs o nazwie "{arg}" został usunięty z listy!\n')
  
  def list(self):
    if self.finished_courses.empty():
      sys.stdout.write('Brak ukończonych kursów na liście\n')
    for name in self.finished_courses.names():
      sys.stdout.write(f'{name}\n')

  def calculate_engineer(self):
    types_lacks, effects_lacks = self.requirements.check_engineer(self.finished_courses.all())

    if types_lacks:
      sys.stdout.write('\n*** Liczba ECTS potrzebna do uzyskania z przedmiotów o typie z danej grupy: ***\n')
    for lack in types_lacks:
      types, ects = lack['types'], lack['ects']
      sys.stdout.write('- ')
      for i, type in enumerate(types, start=1):
        sys.stdout.write(f'{type}: {ects}\n' if i == len(types) else f'{type}, ')

    if effects_lacks:
      sys.stdout.write('\n*** Efekty kształcenia potrzebne do zaliczenia: ***\n')
    for effect in effects_lacks:
      sys.stdout.write(f'- {effect}\n')

  def calculate_bachelor(self):
    types_lacks, effects_lacks = self.requirements.check_bachelor(self.finished_courses.all())

    if types_lacks:
      sys.stdout.write('\n*** Liczba ECTS potrzebna do uzyskania z przedmiotów o typie z danej grupy: ***\n')
    for lack in types_lacks:
      types, ects = lack['types'], lack['ects']
      sys.stdout.write('- ')
      for i, type in enumerate(types, start=1):
        sys.stdout.write(f'{type}: {ects}\n' if i == len(types) else f'{type}, ')

    if effects_lacks:
      sys.stdout.write('\n*** Efekty kształcenia potrzebne do zaliczenia: ***\n')
    for effect in effects_lacks:
      sys.stdout.write(f'- {effect}\n')
  
  def update(self):
    if self.repository.update():
      self.courses = self.repository.find_all()

  def quit(self):
    sys.stdout.write('Do zobaczenia!\n')
    sys.exit()

  def complete_add(self, text, line):
    return self.courses.completions(text, line)

  def complete_rm(self, text, line):
    return self.finished_courses.completions(text, line)

  def default(self, line):
    command = line.partition(' ')[0]
    sys.stdout.write(f'Niepoprawna komenda: "{command}".\nWpisz help lub ?, aby zobaczyć dostępne komendy.\n')