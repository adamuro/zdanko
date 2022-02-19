import getpass
import json
import platform
import sys
from pathlib import Path

class Dotfile:
  def __init__(self):
    if self.__linux():
      self.path = f'/home/{getpass.getuser()}/.zdanko'
    else:
      sys.stderr.write('Program nie jest obsługiwany przez ten system operacyjny :(\n')
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
