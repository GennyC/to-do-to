from flask import Flask, render_template, request, redirect, url_for, session, flash
import models
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key!

# Authentication routes
@app.route("/")
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = models.verify_user(email, password)
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['nombre']
            session['user_email'] = user['email']
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        
        if models.create_user(nombre, email, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email already exists', 'error')
    
    return render_template('register.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

# Protected routes - require login
# Protected routes - require login
@app.route("/home")
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    week_tasks = models.get_tasks_due_this_week(user_id)
    month_tasks = models.get_tasks_due_this_month(user_id)
    all_tasks = models.get_tasks(user_id)
    
    return render_template("home.html", 
                         week_tasks=week_tasks,
                         month_tasks=month_tasks, 
                         all_tasks=all_tasks,
                         current_filter="home",
                         user_name=session.get('user_name'))

@app.route("/todo")
def todo():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    grouped_tasks = models.get_tasks_grouped_by_month("To Do", user_id)
    return render_template("tasks_by_month.html", 
                         grouped_tasks=grouped_tasks, 
                         current_filter="todo", 
                         title="To Do Tasks",
                         user_name=session.get('user_name'))

@app.route("/in-progress")
def in_progress():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    grouped_tasks = models.get_tasks_grouped_by_month("In Progress", user_id)
    return render_template("tasks_by_month.html", 
                         grouped_tasks=grouped_tasks, 
                         current_filter="in-progress", 
                         title="In Progress Tasks",
                         user_name=session.get('user_name'))

@app.route("/done")
def done():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    grouped_tasks = models.get_tasks_grouped_by_month("Done", user_id)
    return render_template("tasks_by_month.html", 
                         grouped_tasks=grouped_tasks, 
                         current_filter="done", 
                         title="Completed Tasks",
                         user_name=session.get('user_name'))

@app.route("/add", methods=["POST"])
def add():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    title = request.form["title"]
    description = request.form["description"]
    due_date = request.form["due_date"]
    user_id = session['user_id']
    models.add_task(title, description, due_date, user_id)
    return redirect("/home")

# The update_status function can remain the same since it updates by task ID
# But you might want to add user verification for extra security:
@app.route("/update/<int:id>/<string:status>")
def update(id, status):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    models.update_status(id, user_id, status)
    referrer = request.headers.get("Referer", "/home")
    return redirect(referrer)

# Add these routes to your app.py

@app.route("/account")
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = models.get_user_by_id(session['user_id'])
    return render_template("account.html", 
                         user=user,
                         current_filter="account",
                         user_name=session.get('user_name'))

@app.route("/update_name", methods=["POST"])
def update_name():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    new_name = request.form['nombre']
    if models.update_user_name(session['user_id'], new_name):
        session['user_name'] = new_name
        flash('Name updated successfully!', 'success')
    else:
        flash('Error updating name', 'error')
    
    return redirect(url_for('account'))

@app.route("/update_password", methods=["POST"])
def update_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    
    # Verify current password
    user = models.verify_user(session['user_email'], current_password)
    if not user:
        flash('Current password is incorrect', 'error')
        return redirect(url_for('account'))
    
    if new_password != confirm_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('account'))
    
    if len(new_password) < 6:
        flash('Password must be at least 6 characters long', 'error')
        return redirect(url_for('account'))
    
    if models.update_user_password(session['user_id'], new_password):
        flash('Password updated successfully!', 'success')
    else:
        flash('Error updating password', 'error')
    
    return redirect(url_for('account'))

@app.route("/delete/<int:id>")
def delete_task(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    success = models.delete_task(id, user_id)
    
    if success:
        flash('Task deleted successfully!', 'success')
    else:
        flash('Task not found or you do not have permission to delete it', 'error')
    
    referrer = request.headers.get("Referer", "/home")
    return redirect(referrer)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
