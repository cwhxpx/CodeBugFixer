from flask import Flask, request, render_template
from openai import OpenAI
import config

app = Flask(__name__)

#OpenAI API KEY
api_key = config.API_KEY
# new openai client
openai_cleint = OpenAI(
    api_key=api_key
)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # code err
        code = request.form["code"]
        error = request.form["error"]
        prompt = (f"Explain the error in this code without fixing it:"
                  f"\n\n{code}\n\nError:\n\n{error}")
        model_engine = "gpt-4o"

        # call openai for explanantion
        explanation_completions = openai_cleint.chat.completions.create(
            model=model_engine,
            messages=[
                {"role":"user","content":prompt}
            ]
        )
        explanation = explanation_completions.choices[0].message.content
        # call openai for fixing codes
        fixed_code_prompt = (
            f"Fix this code: \n\n{code}\n\nError:\n\n{error}."
            f" \n Respond only with the fixed code."
        )

        fixed_code_completions = openai_cleint.chat.completions.create(
            model=model_engine,
            messages=[
                {"role":"user","content":fixed_code_prompt}
            ]
        )
        fixed_code = fixed_code_completions.choices[0].message.content
        #update front page
        return render_template("index.html",
                           explanation=explanation,
                           fixed_code=fixed_code)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()