from flask import Flask, session, render_template, request, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'rock,paper,scissors'
choices = ['rock', 'paper', 'scissors']


def get_winner(user, computer):
    if user == computer:
        return "Draw!"
    if (
        (user == 'rock' and computer == 'scissors') or
        (user == 'paper' and computer == 'rock') or
        (user == 'scissors' and computer == 'paper')
    ):
        return "You win!"
    return "Computer wins!"


@app.route('/')
def home():
    session.setdefault("wins", 0)
    session.setdefault("losses", 0)
    session.setdefault("draws", 0)
    return render_template('index.html', session=session)


@app.route('/play', methods=['POST'])
def play():
    user_choice = request.form['choice'].lower()
    computer_choice = random.choice(choices)
    winner = get_winner(user_choice, computer_choice)

    if winner == "You win!":
        session["wins"] = session.get("wins", 0) + 1
    elif winner == "Computer wins!":
        session["losses"] = session.get("losses", 0) + 1
    else:
        session["draws"] = session.get("draws", 0) + 1

    return render_template(
        'results.html',
        user_choice=user_choice,
        computer_choice=computer_choice,
        winner=winner,
        session=session
    )


@app.route('/reset')
def reset():
    session["wins"] = 0
    session["losses"] = 0
    session["draws"] = 0
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
