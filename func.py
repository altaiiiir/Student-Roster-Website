from flask import Flask, redirect, url_for, render_template, request
import psycopg2

#connect to the local host db
con = psycopg2.connect (
host = "database-finalproject.cwap51qwtcts.us-west-2.rds.amazonaws.com",
database = "webdb",
user = "postgres",
password = "2fD9vPoMU6HAfMM"
)
def viewAdmin():
    cur = con.cursor()
    cur.execute('Select * from Administrator')
    rows = cur.fetchall()

    for i in rows:
        print (i)
    cur.close()
def viewStudents(name):
  cur = con.cursor()
  strname=str(name)
  cur.execute('Select ID, FirstName, LastName, from Student where Student.FirstName = %s', (strname))
  rows = cur.fetchall()
  #for i in rows:
   #   print( i[0])

  cur.close()
  return rows

def viewAllStudents():
    cur = con.cursor()
    allStudentsQuery = "Select * from Student"
    #execute query
    cur.execute(allStudentsQuery)
    rows = cur.fetchall()
    cur.close()
    print(rows)
    return rows
    
def viewStudentNotes():
    cur = con.cursor()
    query = """SELECT Student.StudentID, Note.NoteID, Student.FirstName, Student.LastName,
                                 Note.Note, Note.Date, Note_Type.Name FROM Student_Notes
                   JOIN Note ON (Student_Notes.NoteID = Note.ID)
                   JOIN Note_Type ON (Note.Type = Note_Type.Type)
                   JOIN Student ON (Student_Notes.StudentID = Student.ID)
                    """
    thequery = """select * from Note"""

    cur.execute(query)
    studentNotesRows = cur.fetchall()
    print('---------------')
    print(studentNotesRows)
    #print(studentNotesRows)
    cur.close()
    return studentNotesRows

def viewSpecificStudentNotes(studentID):
    cur = con.cursor()
    ID=int(studentID)
    query = """SELECT Student_Notes.StudentID, Note.NoteID, Student.FirstName, Student.LastName,
                                 Note.Note, Note.Date, Note_Type.Name FROM Student_Notes
                   JOIN Note ON (Student_Notes.NoteID = Note.ID)
                   JOIN Note_Type ON (Note.Type = Note_Type.Type)
                   JOIN Student ON (Student_Notes.StudentID = Student.ID)
                   WHERE student.studentID = %s;
                    """
    cur.execute(query, (ID,))
    rows = cur.fetchall()
  #for i in rows:
   #   print( i[0])

    cur.close()
    return rows