from functools import reduce
from scraper import Scraper

ENGINEER_REQUIREMENTS = {
  'types': [
    { 'types': ['seminarium'], 'ects': 1 },
    { 'types': ['projekt'], 'ects': 1 },
    { 'types': ['informatyczny 1', 'informatyczny inż.'], 'ects': 66 },
    { 'types': ['informatyczny inż.'], 'ects': 12 },
    { 'types': ['kurs inżynierski'], 'ects': 1 },
    { 'types': [
        'obowiązkowy 1',
        'obowiązkowy 2',
        'obowiązkowy 3',
        'informatyczny 1',
        'informatyczny inż.',
        'k1 - kurs podstawowy',
        'k2 - kurs zaawansowany',
        'kurs inżynierski',
        'projekt'
      ], 'ects': 170 }, # Does 'inne' count?
    { 'types': ['humanistyczno-społeczny'], 'ects': 5 }
  ],
  'effects': [
    'podstawy informatyki i programowania',
    'programowanie i projektowanie obiektowe',
    'podstawy inżynierii oprogramowania',
    'architektury systemów komputerowych',
    'systemy operacyjne',
    'sieci komputerowe',
    'bazy danych',
    'inżynieria oprogramowania (l)',
    'rachunek prawdopodobieństwa (i)',
    'społeczno-ekonomiczne aspekty informatyki (i)'
  ]
}

class Requirements:
  def __init__(self, engineer=ENGINEER_REQUIREMENTS):
    self.engineer = engineer
    self.courses = []

  def add_course(self, course):
    if course not in self.courses:
      self.courses.append(course)

  def remove_course(self, course):
    self.courses.remove(course)

  def check_engineer(self):
    types_lacks, effects_lacks = [], []
    for req in self.engineer['types']:
      ects = reduce(lambda sum, c: sum + c['ects'] if c['type'] in req['types'] else sum, self.courses, 0)
      if ects < req['ects']:
        types_lacks.append({ 'types': req['types'], 'ects': req['ects'] - ects })
    for effect in self.engineer['effects']:
      if all(effect not in course['effects'] for course in self.courses):
        effects_lacks.append(effect)

    return { 'types': types_lacks, 'effects': effects_lacks }
