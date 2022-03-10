from flask import Flask, render_template, redirect, request
from functions import send_mail, getcookie, addcookie, delcookies
import datetime
import os
import pytz

app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
utc = pytz.UTC

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/submitform", methods=["POST", "GET"])
def submitform():
  if request.method == "POST":
    lastdone = getcookie("lastdone")
    if lastdone != False:
      timenow = datetime.datetime.now()
      lastdone = lastdone.replace(tzinfo=utc)
      timenow = timenow.replace(tzinfo=utc)
      onehour = datetime.timedelta(hours=1)
      lastdone = lastdone + onehour
      if lastdone > timenow:
        return "You can do the form at most once every hour!"
      delcookies()
    title = request.form["title"]
    email = request.form["email"]
    description = request.form["description"]
    send_mail(title, email, description)
    addcookie("lastdone", datetime.datetime.now())
    return "done!"
  else:
    return redirect("/")