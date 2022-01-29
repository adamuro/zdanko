import getpass
import json
from pathlib import Path
import platform
import sys

class Dotfile:
  def __init__(self, path=None):
    if path:
      self.path = path
    elif self.__linux():
      self.path = f'/home/{getpass.getuser()}/.zdanko'
    # elif self.__windows():
    #   self.path = f'C:/{getpass.getuser()}/AppData/Roaming/Zdanko/courses.json'
    else:
      sys.stderr('Program nie jest obsługiwany przez ten system operacyjny :(\n')
      sys.exit()
    
    Path(self.path).touch(exist_ok=True)
    
  def __linux(self):
    return platform.system() == 'Linux'

  def load(self):
    courses_json = open(self.path, 'r').read()
    return json.loads(courses_json) if courses_json else []
  
  def save(self, courses):
    file = open(self.path, 'w')
    file.write(json.dumps(courses))

  # def __windows(self):
  #   return platform.system() == 'Windows'
