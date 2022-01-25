import config
from pymongo import MongoClient
from scraper import Scraper

class CoursesRepository:
  def __init__(self):
    self.courses = MongoClient(config.DB_URI)['zdanko']['courses']

  def find_all(self):
    return list(self.courses.find({}, { '_id': False }))
  
  def find_by_name(self, name):
    return self.courses.find_one({ 'name': name })

  def update(self):
    updated_courses = Scraper().courses
    current_courses = self.find_all()
    key = lambda course: course['name']

    if sorted(updated_courses, key=key) != sorted(current_courses, key=key):
      self.courses.drop()
      self.courses.insert_many(updated_courses)
      print('Kursy zostały uaktualnione!')
      return True
    else:
      print('Kursy nie wymagają aktualizacji.')
      return False

class CoursesList:
  def __init__(self, courses: list=[]):
    self.courses = courses
  
  def all(self):
    return self.courses
  
  def names(self):
    return [course['name'] for course in self.courses]
  
  def name(self, name):
    matches = [course for course in self.courses if course['name'] == name]
    return matches[0] if len(matches) == 1 else None
  
  def add(self, course):
    self.courses.append(course)

  def remove(self, course):
    if course not in self.courses:
      return False

    self.courses.remove(course)
    return True
  
  def empty(self):
    return len(self.courses) == 0
  
  def completions(self, text, line):
    # Cmd autocompletes only the last word so we need to skip all the words before (offset)
    arg = line.partition(' ')[2].lower()
    offset = len(arg) - len(text)
    return [course['name'][offset:] for course in self.courses if course['name'].startswith(arg)]


