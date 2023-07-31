#!/usr/bin/env python3
import cgi
import cgitb
import pymysql

cgitb.enable()

print("Content-Type:text/html; charset=utf-8")
print()


# Function to calculate the average score
def calculate_average(midterm_exam1, midterm_exam2, final_exam):
    return (midterm_exam1 + midterm_exam2 + 2 * final_exam) / 4

print("Content-type: text/html\n")

# Connect to the MySQL database (make sure to replace the placeholders with your actual database credentials)
db = pymysql.connect(host='localhost', user='root', passwd='Kiran@123#', db='studentdb')
cursor = db.cursor()

# Get form data
form = cgi.FieldStorage()

# Check if 'action' parameter exists in the form
if 'action' in form:
    action = form['action'].value
    print("action: " + action)  # Moved the print statement outside the 'if' block
    if action == 'insert':
        # Get student details from the form
        student_name = form['student_name'].value
        midterm_exam1 = float(form['midterm_exam1'].value)
        midterm_exam2 = float(form['midterm_exam2'].value)
        final_exam = float(form['final_exam'].value)

        # Calculate average score
        average_score = calculate_average(midterm_exam1, midterm_exam2, final_exam)

        # Insert the new record into the database
        query = "INSERT INTO student_grades (name, midterm_1, midterm_2, final_exam, average_score) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (student_name, midterm_exam1, midterm_exam2, final_exam, average_score))
        db.commit()
    elif action == 'delete':
        print("No action specified.")  # Print statement inside the 'else' block

        # Get student ID from the form
        student_id = form['delete_name'].value

        # Delete the record from the database
        query = "DELETE FROM student_grades WHERE name = %s"
        cursor.execute(query, (student_id,))
        db.commit()

# Fetch all records from the database
query = "SELECT name, average_score FROM student_grades"
cursor.execute(query)
rows = cursor.fetchall()

# HTML display of the student table
print("<html><body>")
print("<h2>Student List</h2>")
print("<table border='1'>")
print("<tr><th>Name</th><th>Average Score</th></tr>")
for row in rows:
    name, average_score = row
    print("<tr>")
    print(f"<td>{name}</td><td>{average_score:.2f}</td>")
    print(f"<td><form action='lab08.py' method='post'>")
    print("</form></td>")
    print("</tr>")
print("</table>")

print("</body></html>")

# Close the database connection
db.close()


