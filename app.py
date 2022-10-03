import datetime
from flask import Flask, render_template, request

app = Flask(__name__)
jobs = ["Test habit", "Test habit 2", "Test habit 3"]


@app.context_processor
def add_calc_date_range():
    def date_range(start: datetime.date):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    return {"date_range": date_range}


@app.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
    else:
        selected_date = datetime.date.today()

    return render_template(
        "index.html",
        jobs=jobs,
        title="Job list - Home",
        selected_date=selected_date
    )


@app.route("/add", methods=["GET", "POST"])
def add_job():
    if request.method == "POST":
        jobs.append(request.form.get("job"))
    return render_template("add_job.html",
                           title="Job list - Add Job",
                           selected_date=datetime.date.today(),
                           )
