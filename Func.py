from flask import Flask, redirect, url_for, render_template, request
import psycopg2

#connect to the local host db
con = psycopg2.connect (
host = "database-finalproject.cwap51qwtcts.us-west-2.rds.amazonaws.com",
database = "webdb",
user = "postgres",
password = "2fD9vPoMU6HAfMM"
)

def viewStudents():
    result = ""
    cur.execute('Select * from Student')
    rows = cur.fetchall()

    for r in rows:
        print(f"ID {r[0]} name {r[1]}")

