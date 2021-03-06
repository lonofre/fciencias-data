from collections import namedtuple

Course = namedtuple('Course', 'id name semester plan classes')
Professor = namedtuple('Professor', 'id role name')
Hours = namedtuple('Hours', 'days start end')
ClassData = namedtuple('ClassData', 'group staff enrolled quota schedule') 


