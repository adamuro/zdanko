from os import getenv
from typing import List
from dotenv import load_dotenv
from pymongo import MongoClient

from scraper import Scraper

class CoursesRepository:
  def __init__(self):
    load_dotenv()
    db_password = getenv('DB_PASSWORD')
    db_uri = getenv('DB_URI').replace('<password>', db_password)
    self.courses = MongoClient(db_uri)['zdanko']['courses']

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
  def __init__(self, courses: List=[]):
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

