from flask import Flask, render_template, request, flash, redirect, url_for, session
import os
import random

app = Flask(__name__)


@app.route("/recommandations", methods=["GET", "POST"])
def fetch_recs():
    x = random.randint(1, 9999)
    
    return render_template("index.html", Recommandation_text="Below are the recommendations", p1="a".format(x), p2="a2".format(x),p3="a".format(x), p4="a2".format(x),p5="a".format(x))


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
