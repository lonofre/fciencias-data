from peewee import *

database = SqliteDatabase('fciencias.db')

class BaseModel(Model):
    class Meta:
        database = database

class Subject(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()

class Plan(BaseModel):
    id = IntegerField()

class Belongs(BaseModel):
    '''Many to many relationship between Subject and Plan'''
    
    plan = ForeignKeyField(Plan, backref='subjects')
    subject = ForeignKeyField(Subject, backref='plans')

class ClassData(BaseModel):
    id = IntegerField(primary_key=True)
    group = IntegerField()
    enrolled = IntegerField(null = False)
    quota = IntegerField(null = False)
    semester = IntegerField()
    subject = ForeignKeyField(Subject, backref='classes')

class Professor(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()

class Staff(BaseModel):
    '''Many to many between a Class and a Professor with
    her spefic role'''

    professor = ForeignKeyField(Professor, backref='classes')
    class_data = ForeignKeyField(ClassData, backref='professors')
    role = CharField()

class Hour(BaseModel):
    id = IntegerField(primary_key=True)
    start = TimeField(formats = 'HH:MM')
    end = TimeField(formats = 'HH:MM')

class Schedule(BaseModel):
    id = IntegerField(primary_key=True)
    hour = ForeignKeyField(Hour, backref = 'schedules')
    day = CharField()

class IsImparted(BaseModel):
    '''Many to many relationship, which was made to reduce redundancy'''

    classData = ForeignKeyField(ClassData, backref = 'schedule')
    schedule = ForeignKeyField(Schedule, backref = 'classes')


def create_tables():
    with database:
        tables = [Subject, Plan, Belongs, ClassData, Professor, Staff,
                Hour, Schedule, IsImparted]
        database.create_tables(tables)
