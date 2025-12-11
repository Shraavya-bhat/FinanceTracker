from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from models import db, Transaction
from datetime import datetime
import os
import io
import pandas as pd

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "finance.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Ensure DB exists
with app.app_context():
    db.create_all()

# ------- Helper ----------
def parse_iso(dt_str):
    try:
        return datetime.fromisoformat(dt_str)
    except Exception:
        return datetime.now()

# ------- Routes ----------
@app.route("/")
def index():
    # Dashboard summary
    txs = Transaction.query.order_by(Transaction.date.desc()).limit(10).all()
    all_txs = Transaction.query.all()
    income = sum(t.amount for t in all_txs if t.type == "income")
    expense = sum(t.amount for t in all_txs if t.type == "expense")
    balance = income - expense
    return render_template("index.html",
                           transactions=txs,
                           income=income,
                           expense=expense,
                           balance=balance)

@app.route("/add", methods=["GET", "POST"])
def add_tx():
    if request.method == "POST":
        ttype = request.form.get("type")
        amount = float(request.form.get("amount") or 0)
        category = request.form.get("category") or "Other"
        note = request.form.get("note") or ""
        date = request.form.get("date") or datetime.now().isoformat()

        tx = Transaction(type=ttype, amount=amount, category=category, date=date, note=note)
        db.session.add(tx)
        db.session.commit()
        return redirect(url_for("index"))

    # default categories for forms
    income_categories = ["salary", "bonus", "interest", "gift", "other"]
    expense_categories = ["food", "rent", "travel", "shopping", "bills", "other"]
    return render_template("add.html",
                           income_categories=income_categories,
                           expense_categories=expense_categories)

@app.route("/transactions")
def transactions():
    q = request.args.get("q", "").strip()
    if q:
        # simple search across category and note
        txs = Transaction.query.filter(
            (Transaction.category.ilike(f"%{q}%")) |
            (Transaction.note.ilike(f"%{q}%"))
        ).order_by(Transaction.date.desc()).all()
    else:
        txs = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template("transactions.html", transactions=txs, q=q)

@app.route("/edit/<int:tx_id>", methods=["GET", "POST"])
def edit(tx_id):
    tx = Transaction.query.get_or_404(tx_id)
    if request.method == "POST":
        tx.type = request.form.get("type")
        tx.amount = float(request.form.get("amount"))
        tx.category = request.form.get("category")
        tx.note = request.form.get("note")
        tx.date = request.form.get("date")
        db.session.commit()
        return redirect(url_for("transactions"))
    income_categories = ["salary", "bonus", "interest", "gift", "other"]
    expense_categories = ["food", "rent", "travel", "shopping", "bills", "other"]
    return render_template("edit.html", tx=tx,
                           income_categories=income_categories,
                           expense_categories=expense_categories)

@app.route("/delete/<int:tx_id>", methods=["POST"])
def delete(tx_id):
    tx = Transaction.query.get_or_404(tx_id)
    db.session.delete(tx)
    db.session.commit()
    return redirect(url_for("transactions"))

# ----- API endpoints for charts and reports -----
@app.route("/api/summary")
def api_summary():
    all_txs = Transaction.query.all()
    income = sum(t.amount for t in all_txs if t.type == "income")
    expense = sum(t.amount for t in all_txs if t.type == "expense")
    balance = income - expense
    return jsonify({"income": income, "expense": expense, "balance": balance})

@app.route("/api/category_data")
def api_category_data():
    # expense by category (all-time)
    txs = Transaction.query.filter_by(type="expense").all()
    df = pd.DataFrame([t.to_dict() for t in txs])
    if df.empty:
        return jsonify({"labels": [], "values": []})
    grouped = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    return jsonify({"labels": grouped.index.tolist(), "values": grouped.values.tolist()})

@app.route("/export")
def export_csv():
    txs = Transaction.query.order_by(Transaction.date.desc()).all()
    df = pd.DataFrame([t.to_dict() for t in txs])
    if df.empty:
        # return empty csv
        csv_bytes = "id,type,amount,category,date,note\n".encode()
    else:
        csv_bytes = df.to_csv(index=False).encode()

    buffer = io.BytesIO(csv_bytes)
    buffer.seek(0)
    return send_file(buffer, mimetype="text/csv", download_name="transactions.csv", as_attachment=True)

# ------- run ----------
if __name__ == "__main__":
    app.run(debug=True)
