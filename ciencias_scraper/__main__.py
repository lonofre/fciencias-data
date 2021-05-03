import sys
import time
import re
from .persistence import save_all_data, course_exists, course_semester_exists, assign_plan
from .scraper import major_urls, course_urls, course_data
from .models import Course, create_tables

request_delay = 10

def scrap_semester(semester = ''):
    '''Extrat data from a given semester, for instance, 20201, 20202'''

    try:
        majors = major_urls(semester)
    except:
        print('Cannot find given semester')
        sys.exit()

    total_majors = len(majors)
    print(f'- Majors to scrap: {total_majors}')
    create_tables()
    for count, major in enumerate(majors, start = 1):
        urls = course_urls(major)

        for course_url in urls:
            semester, plan, id_course = re.findall(r'\d+', course_url)
            course = None
            if not course_exists(id_course) or not course_semester_exists(id_course, semester):
                course = course_data(course_url)
                save_all_data(course)
                time.sleep(request_delay)
            else:
                course = Course.get_by_id(id_course)
                assign_plan(course, plan)
            
            print(f'-- "{course.name}" saved')

        print(f'- Complete {count}/{total_majors}\n')



semester = ''
if len(sys.argv) > 1:
    semester = sys.argv[1]

scrap_semester(semester)
