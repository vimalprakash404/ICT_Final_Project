from flask import Flask, render_template,request, redirect

import mysql.connector

app = Flask(__name__)
app = Flask(__name__,static_folder='static/css',static_url_path='')
db = mysql.connector.connect(
    host='username.mysql.pythonanywhere-services.com',
    user='vimalprakash404',
    password='host1234',
    database='vimalprakash404$ICT_EMPLOYEE'
)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

       

        if username == 'admin' and password == 'admin123':
            
            return redirect('/dashboard')
        else:
            
            error_message = 'Invalid username or password'  

            return render_template('login.html', error_message=error_message)

   
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template('dashboard.html', employees=employees)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form.get('name')
        department = request.form.get('department')
        salary = request.form.get('salary')

        
        cursor = db.cursor()
        query = "INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, department, salary))
        db.commit()

        return redirect('/dashboard')  

    return render_template('add_employee.html')

@app.route('/delete_employee/<employee_id>')
def delete_employee(employee_id):
    
    cursor = db.cursor()
    query = "DELETE FROM employees WHERE id = %s"
    cursor.execute(query, (employee_id,))
    db.commit()

    return redirect('/dashboard') 

@app.route('/edit_employee/<employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    cursor = db.cursor()
    if request.method == 'POST':
        name = request.form.get('name')
        department = request.form.get('department')
        salary = request.form.get('salary')

        
        query = "UPDATE employees SET name = %s, department = %s, salary = %s WHERE id = %s"
        cursor.execute(query, (name, department, salary, employee_id))
        db.commit()

        return redirect('/dashboard')  
    else:
        
        query = "SELECT * FROM employees WHERE id = %s"
        cursor.execute(query, (employee_id,))
        employee = cursor.fetchone()

        return render_template('edit_employee.html', employee=employee)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        search_type = request.form.get('search_type')

        
        cursor = db.cursor()
        query = "SELECT * FROM employees WHERE {} LIKE %s".format(search_type)
        cursor.execute(query, ('%' + search_query + '%',))
        employees = cursor.fetchall()

        return render_template('search_results.html', employees=employees, search_query=search_query, search_type=search_type)

    return render_template('search.html')
if __name__ == '__main__':
    app.run(debug=True)