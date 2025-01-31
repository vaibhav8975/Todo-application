from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite Database in the Current Working Directory
BASE_DIR = os.path.abspath(os.getcwd())  # Get current working directory
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR}/todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# Define Todo Model
class Todo(db.Model): 
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    des = db.Column(db.String(500), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

# Home Route - List all todos & Add a new one
@app.route("/", methods=['GET', 'POST'])
def index(): 
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if title and desc:
            todo = Todo(title=title, des=desc)
            db.session.add(todo)
            db.session.commit()
    allTodo = Todo.query.order_by(Todo.date_time.desc()).all()
    return render_template('index.html', allTodo=allTodo)

# Delete Todo Route
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# Update Todo Route
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.des = request.form['desc']
        db.session.commit()
        return redirect("/")
    return render_template('update.html', todo=todo)

# Run the Flask app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the database is created in the current directory
    app.run(debug=True)
