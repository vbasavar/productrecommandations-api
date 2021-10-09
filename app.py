from flask import Flask, render_template, request, flash, redirect, url_for, session
import os
import random

app = Flask(__name__)


@app.route("/recommandations", methods=["GET", "POST"])
def fetch_recs():
    return render_template("index.html", Recommandation_text="Below are the recommendations", p1="a", p2="a2",p3="a", p4="a2",p5="a")


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
