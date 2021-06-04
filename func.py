from flask import Flask, redirect, url_for, render_template, request
import psycopg2

#connect to the local host db
con = psycopg2.connect (
host = "database-finalproject.cwap51qwtcts.us-west-2.rds.amazonaws.com",
database = "webdb",
user = "postgres",
password = "2fD9vPoMU6HAfMM"
)

def viewStudents(name):
  cur = con.cursor()
  strname=str(name)
  cur.execute('Select ID, FirstName, LastName, from Student where Student.FirstName = %s', (strname))
  rows = cur.fetchall()
  for i in rows:
      print( i[0])

  cur.close()
  return rows

def viewAllStudents():
    cur = con.cursor()
    allStudentsQuery = "Select * from Student"
    #execute query
    cur.execute(allStudentsQuery)
    rows = cur.fetchall()
    cur.close()
    return rows
    
def viewStudentNotes():
    cur = con.cursor()
    query = """SELECT Student_Notes.StudentID, Note.NoteID, Note.Note, Date, Note.Type FROM Student_Notes
                   JOIN Note ON (Student_Notes.NoteID = Note.ID)
    """
    cur.execute(query)
    studentNotesRows = cur.fetchall()
    cur.close()
    return studentNotesRows
