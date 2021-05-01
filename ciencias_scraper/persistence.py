from .models import *

def save_all_data(course_data: tuple):
    '''Saves all the course data, which includes classes
    professors and schedules'''
    create_tables()

    course = save_course(course_data)
    _, _, semester, id_plan, classes = course_data 
    new_plan = save_plan(id_plan)
    assign_plan(course, new_plan)

    for one_class in classes:
        class_data = save_class_data(one_class, course, semester)
        _, staff, _, _, schedule = one_class
    
        for professor in staff:
            new_professor = save_professor(professor)
            _, role, _ = professor
            assign_class(new_professor, class_data, role)
    
        for class_schedule in schedule:
            days, start, end = class_schedule
            hour = save_hour(start,end)
            
            for day in days:
                new_schedule = save_schedule(day, hour)
                assign_schedule(class_data, new_schedule)


def save_course(course_data: tuple) -> Course:
    '''Saves or gets an existing course

    Parameters
        course_data (tuple(id,name,semester,plan,classes))

    Returs
        Course: the course saved
    '''

    id_course, course_name, semester, plan, _ = course_data
    course, _ = Course.get_or_create(
            id = id_course, 
            defaults = {'name': course_name})
    return course


def save_class_data(class_data: tuple, course: Course, semester: int) -> ClassData:
    '''Saves or gets an existing a class
    
    Parameters
        class_data (tuple(group,staff,enrolled,quota,schedule))
        course (Course)
        semester (int)

    Returns
        ClassData: The class saved
    '''

    group, _, enrolled, quota, _ = class_data
    new_class, _ = ClassData.get_or_create(
            group = group,
            semester = semester,
            defaults = {
                'enrolled': enrolled,
                'quota': quota,
                'course': course})

    return new_class


def save_professor(professor_data: tuple) -> Professor:
    '''Saves or gets an existing professor
    
    Parameters
        professor_data (tuple(id, role, name)): a tuple with 
        the professor's data

    Returns
        Professor: the professor created 
    '''

    id_professor, role, name = professor_data
    professor, _ = Professor.get_or_create(
            id = id_professor,
            defaults = {'name': name})
    return professor


def assign_class(professor: Professor, class_data: ClassData, role: str) -> Staff:
    '''Asigns a professor to her class'''

    staff, _  = Staff.get_or_create(professor = professor, 
            class_data = class_data, 
            role = role)
    return staff


def save_plan(plan_number: int) -> Plan:
    '''Saves or gets an existing plan'''

    plan, _ = Plan.get_or_create(id = plan_number)
    return plan

def assign_plan(course: Course, plan: Plan) -> Belongs:
    '''Assigns a study plan to a course'''

    belongs, _ = Belongs.get_or_create(course = course, plan = plan)
    return belongs


def save_hour(start_time: str, end_time: str) -> Hour:
    '''Saves or gets an existing hour'''
    
    hour, _ = Hour.get_or_create(
            start = start_time,
            end = end_time)
    return hour


def save_schedule(day: str, hour: Hour):
    '''Saves or gets an existing schedule'''

    schedule, _ = Schedule.get_or_create(
            day = day,
            hour = hour)
    return schedule


def assign_schedule(class_data: ClassData, schedule: Schedule)-> IsImparted:
    '''Asigns an exchedule to a class'''

    assigned_schedule, _ = IsImparted.get_or_create(
            class_data = class_data,
            schedule = schedule)

    return assigned_schedule
