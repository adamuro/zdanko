from functools import reduce
from scraper import Scraper

ENGINEER_REQUIREMENTS = {
  'types': [
    { 'types': ['projekt'], 'ects': 1 },
    { 'types': ['seminarium'], 'ects': 1 },
    { 'types': ['kurs inżynierski'], 'ects': 1 },
    { 'types': ['informatyczny inż.'], 'ects': 12 },
    { 'types': ['humanistyczno-społeczny'], 'ects': 5 },
    { 'types': ['informatyczny 1', 'informatyczny inż.'], 'ects': 66 },
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
    'społeczno-ekonomiczne aspekty informatyki (i)',
  ],
}

class Requirements:
  def __init__(self, engineer=ENGINEER_REQUIREMENTS):
    self.engineer = engineer

  def check_engineer(self, courses):
    types_lacks, effects_lacks = [], []
    for req in self.engineer['types']:
      ects = reduce(lambda sum, c: sum + c['ects'] if c['type'] in req['types'] else sum, courses, 0)
      if ects < req['ects']:
        types_lacks.append({ 'types': req['types'], 'ects': req['ects'] - ects })
    for effect in self.engineer['effects']:
      if all(effect not in course['effects'] for course in courses):
        effects_lacks.append(effect)

    return types_lacks, effects_lacks
