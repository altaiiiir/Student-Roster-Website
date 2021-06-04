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

def viewStudentNotes():
    cur = con.cursor()
    cur.execute('SELECT * FROM Student_Notes')
    studentNotesRows = cur.fetchall()
    cur.close()
    return studentNotesRows
