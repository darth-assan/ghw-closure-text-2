import os
import random
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def create_ctest(text):
    words = text.split()
    modified_words = []
    for i, word in enumerate(words):
        if i % 2 == 1:
            half_length = len(word) // 2
            modified_word = word[:half_length] + "_" * half_length
            modified_words.append(modified_word)
        else:
            modified_words.append(word)
    ctest = " ".join(modified_words)
    return ctest


def read_random_sample():
    samples_path = "samples.json"
    with open(samples_path, "r", encoding="utf-8") as file:
        samples = json.load(file)
    random_key = random.choice(list(samples.keys()))
    content = samples[random_key]
    return content


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "input_text" in request.form:
            input_text = request.form["input_text"]
            ctest = create_ctest(input_text)
            return render_template("index.html", input_text=input_text, ctest=ctest)
    return render_template("index.html")


@app.route("/generate_sample_ctest", methods=["POST"])
def generate_sample_ctest():
    input_text = read_random_sample()
    ctest = create_ctest(input_text)

    # Create a dictionary to hold both the input_text and ctest
    response_data = {"input_text": input_text, "ctest": ctest}

    # Return the data as JSON
    return response_data


if __name__ == "__main__":
    app.run(debug=True)
