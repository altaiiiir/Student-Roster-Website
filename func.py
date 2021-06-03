from flask import Flask, redirect, url_for, render_template, request
import psycopg2

#connect to the local host db
con = psycopg2.connect (
host = "database-finalproject.cwap51qwtcts.us-west-2.rds.amazonaws.com",
database = "webdb",
user = "postgres",
password = "2fD9vPoMU6HAfMM"
)

def viewCourseCatalog():
    cur = con.cursor()
    cur.execute('Select * from course_catalog')
    rows = cur.fetchall()

    #for r in rows:
   #     print(f"SLN {r[0]} Name {r[1]} CourseCredits {r[2]} Type {r[3]} ")
    # close cursor
    return rows
viewCourseCatalog()

#close the connection
