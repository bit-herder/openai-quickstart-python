import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        medium = request.form["medium"]
        materials = request.form["materials"]
        description = request.form["description"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(medium,materials,description),
            temperature=.5,
            max_tokens=200
        )
        print(response)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)

def generate_prompt(medium,materials,description):
    return """Suggest three names and descriptions for a piece of art in the medium provided. Use the Materials and Description provided below to add flavor to the description you write. Imagine you are writing from the perspective of a new york times art critic, but you also want the pieces to sell. Be very flowery and colorful with your language. 

Medium: {}
Materials: {}
Description: {}
Names and Description:""".format(
        medium.capitalize(),
        materials.capitalize(),
        description.capitalize()
    )
