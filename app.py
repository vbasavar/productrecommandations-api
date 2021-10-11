from flask import Flask, render_template, request, flash, redirect, url_for, session
import os
import random
import pickle
import pandas as pd
import logging
from scipy.sparse import hstack
from utils import preprocess

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route("/recommandations", methods=["GET", "POST"])
def fetch_recs():
    x = random.randint(1, 9999)
    user_details = pd.read_csv("User_products.csv")
    user_ratings = pd.read_csv("final_ratings.csv")
    rfc = pickle.load(open("category_model_allG_rfc.pkl", "rb"))
    vect = pickle.load(open("category_model_allG_vect.pkl", "rb"))
    vect1 = pickle.load(open("category_model_allG_vect1.pkl", "rb"))
    user = request.form['user_id']

    try:
        user_id = user_details['user_id'][user_details['reviews_username'] == user].iloc[0]
    except Exception as e:
        return render_template("index.html", user_not_found="USER NOT FOUND !!. SEARCH AGAIN WITH DIFFERENT USER")

    prods = list(user_ratings.loc[user_id].sort_values(ascending=False)[0:20].to_dict())
    app.logger.info(f"user id : {user_id}")
    app.logger.info(f"prods are : {prods}")
    pos = []
    for i in prods:
        feedback = []
        for line in user_details[['reviews_text', 'reviews_title']][user_details['product_id'] == int(i)].head(
                10).itertuples():
            app.logger.info(f"title : {line[1]}")
            feedback.append(
                rfc.predict(hstack((vect.transform([preprocess(line[2])]), vect1.transform([preprocess(line[1])]))))[0])
        if feedback.count('Positive') > feedback.count('Negative'):
            pos.append(int(i))
        # app.logger.info(f"{i} : {pos}, {feedback}")
    products = user_details[user_details['product_id'].isin(pos)]['name'].unique().tolist()
    # app.logger.info(f"Products are : {products}")
    if len(products) >= 5:
        return render_template("index.html", Recommandation_text="Below are the recommendations\n",
                               products=products[1:5])
    else:
        return render_template("index.html", Recommandation_text="Below are the recommendations\n", products=products)


@app.route("/")
def home():
    app.logger.info("HEllo world")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
