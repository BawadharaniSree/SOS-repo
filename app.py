from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# Function to connect to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',       # Replace with your host
            database='sos_app',     # Replace with your database name
            user='root',            # Replace with your username
            password='Vasu3024.' # Replace with your password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Route to display the login page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    identifier = request.form['identifier']  # This can be either email or mobile
    password = request.form['password']

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)

            # Query to check if the identifier matches either email or mobile
            query = "SELECT * FROM users WHERE (email = %s OR mobile = %s) AND password = %s"
            cursor.execute(query, (identifier, identifier, password))
            user = cursor.fetchone()

            if user:
                session['user_id'] = user['id']  # Store user ID in session
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials.", "danger")
                return redirect(url_for('index'))
        except Error as e:
            flash(f"Database error: {e}", "danger")
            return redirect(url_for('index'))
        finally:
            cursor.close()
            connection.close()
    else:
        flash("Database connection failed.", "danger")
        return redirect(url_for('index'))

# Route to display the signup page
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

# Route to handle signup form submission
@app.route('/signup', methods=['POST'])
def signup():
    fullname = request.form['fullname']
    email = request.form['email']
    mobile = request.form['mobile']
    address = request.form['address']
    aadhar = request.form['aadhar']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    # Validate password confirmation
    if password != confirm_password:
        flash("Passwords do not match!", "danger")
        return redirect(url_for('signup_page'))

    # Connect to the database
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Check if the email or mobile already exists
            query_check = "SELECT * FROM users WHERE email = %s OR mobile = %s"
            cursor.execute(query_check, (email, mobile))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("User with this email or mobile already exists!", "danger")
                return redirect(url_for('signup_page'))

            # Insert the new user into the database
            query_insert = """
                INSERT INTO users (fullname, email, mobile, address, aadhar, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_insert, (fullname, email, mobile, address, aadhar, password))
            connection.commit()

            flash("Signup successful! Please log in.", "success")
            return redirect(url_for('index'))  # Redirect to login page after signup
        except Error as e:
            flash(f"Database error: {e}", "danger")
            return redirect(url_for('signup_page'))
        finally:
            cursor.close()
            connection.close()
    else:
        flash("Database connection failed.", "danger")
        return redirect(url_for('signup_page'))

# Route to display the dashboard after successful login
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("You need to log in first.", "danger")
        return redirect(url_for('index'))

    user_id = session['user_id']
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT fullname, email, mobile, address, aadhar FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()

            if user:
                return f"""
                    <h2>Welcome, {user['fullname']}!</h2>
                    <p><strong>Email:</strong> {user['email']}</p>
                    <p><strong>Mobile:</strong> {user['mobile']}</p>
                    <p><strong>Address:</strong> {user['address']}</p>
                    <p><strong>Aadhar:</strong> {user['aadhar']}</p>
                    <a href="/logout">Logout</a>
                """
            else:
                flash("User not found.", "danger")
                return redirect(url_for('index'))
        except Error as e:
            flash(f"Database error: {e}", "danger")
            return redirect(url_for('index'))
        finally:
            cursor.close()
            connection.close()
    else:
        flash("Database connection failed.", "danger")
        return redirect(url_for('index'))

# Route to handle logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)