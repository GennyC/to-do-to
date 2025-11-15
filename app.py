from flask import Flask, render_template, request, redirect
import models

app = Flask(__name__)

@app.route("/")
def home():
    tasks = models.get_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    description = request.form["description"]
    due_date = request.form["due_date"]
    models.add_task(title, description, due_date)
    return redirect("/")

@app.route("/update/<int:id>/<string:status>")
def update(id, status):
    models.update_status(id, status)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
