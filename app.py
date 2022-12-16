import os

#import openai
from flask import Flask, redirect, render_template, request, url_for
from transformers import pipeline, set_seed

app = Flask(__name__)
#openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key =''

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        generator = pipeline('text-generation', model='gpt2')
        set_seed(42)
        # import warnings
        # warnings.filterwarnings("ignore")
        gen=generator(animal, max_length=70, num_return_sequences=7)
        #for i in range(7):
        #print([i+1], gen[i].get("generated_text"),'\n') 
        #return redirect(url_for("index", result=response.choices[0].text))
        return redirect(url_for("index", result=gen[0].get("generated_text")))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
