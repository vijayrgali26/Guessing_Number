from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    start = int(request.form['start'])
    end = int(request.form['end'])
    session['start'] = start
    session['end'] = end
    session['mid'] = (start + end) // 2
    return jsonify({"guess": session['mid']})

@app.route('/respond', methods=['POST'])
def respond():
    response = request.form['response']
    mid = session['mid']

    if response == 'yes':
        return jsonify({"message": f"Yes! I have guessed it: {mid}", "done": True})
    elif response == 'greater':
        session['start'] = mid + 1
    elif response == 'lesser':
        session['end'] = mid - 1

    if session['start'] > session['end']:
        return jsonify({"message": "Couldn't guess it. Are your answers correct?", "done": True})

    session['mid'] = (session['start'] + session['end']) // 2
    return jsonify({"guess": session['mid'], "done": False})

if __name__ == '__main__':
    app.run(debug=True)
