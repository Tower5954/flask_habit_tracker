import datetime
import uuid
from flask import Blueprint, current_app, render_template, request, redirect, url_for

pages = Blueprint("jobs", __name__, template_folder="templates", static_folder="static")


@pages.context_processor
def add_calc_date_range():
    def date_range(start: datetime.datetime):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    return {"date_range": date_range}


def today_at_midnight():
    today = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day)


@pages.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    else:
        selected_date = today_at_midnight()

    jobs_on_date = current_app.db.habits.find({"added": {"$lte": selected_date}})
    completions = [
        job["job"]
        for job in current_app.db.completions.find({"date": selected_date})
    ]

    return render_template(
        "index.html",
        jobs=jobs_on_date,
        completions=completions,
        title="Job list - Home",
        selected_date=selected_date
    )


@pages.route("/add", methods=["GET", "POST"])
def add_job():
    today = today_at_midnight()
    if request.form:
        current_app.db.habits.insert_one(
            {"_id": uuid.uuid4().hex, "added": today, "name": request.form.get("job")}
        )
    return render_template("add_job.html",
                           title="Job list - Add Job",
                           selected_date=today,
                           )


@pages.route("/complete", methods=["POST"])
def complete():
    date_string = request.form.get("date")
    job = request.form.get("jobId")
    date = datetime.datetime.fromisoformat(date_string)
    current_app.db.completions.insert_one({"date": date, "job": job})

    return redirect(url_for("jobs.index", date=date_string))