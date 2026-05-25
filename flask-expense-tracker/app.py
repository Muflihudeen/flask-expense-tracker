from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)

class Transaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    amount = db.Column(db.Float, nullable=False)

    type = db.Column(db.String(20), nullable=False)

    category = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    
    transactions = Transaction.query.all()

    balance = 0
    for transaction in transactions:
        if transaction.type == "income":
            balance += transaction.amount
        else:
            balance -= transaction.amount

    return render_template("index.html", transactions=transactions, balance=balance)

@app.route("/add", methods=["GET", "POST"])
def add_transaction():

    if request.method == "POST":

        tittle = request.form.get("title")

        amount = float(request.form.get("amount"))

        transaction_type = request.form.get("type")

        category = request.form.get("category")

        new_transaction = Transaction(title=tittle, amount=amount, type=transaction_type, category=category)

        db.session.add(new_transaction)

        db.session.commit() 

        return redirect("/")
    return render_template("add_transaction.html")

@app.route("/delete/<int:id>")
def delete_transaction(id):

    transaction = Transaction.query.get(id)

    if transaction:

        db.session.delete(transaction)

        db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)        