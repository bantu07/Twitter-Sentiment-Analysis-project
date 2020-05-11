import json

from flask import Flask, render_template, request

from tweets import QueryTwitter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        search = request.form["srch-term"]
        (z, x, y, c, d, a, b, n) = QueryTwitter(search)
        return render_template('result.html', emotion_plot=z, word_freqs=x, max_freq=y, source_plot=json.dumps(c),
                               sentiment_pie=json.dumps(d), table=json.dumps(a),subjective_plot=json.dumps(b),
                               lda_table=json.dumps(n), search=search)


if __name__ == "__main__":
    app.run(debug=True)

