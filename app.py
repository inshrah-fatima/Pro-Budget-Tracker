from flask import Flask, render_template, request, redirect, url_for, flash
import os
from models.user import User
from models.income import Income
from models.expense import Expense
from models.budget import Budget
from models.goal import Goal
from storage.json_storage import JSONStorage
from storage.csv_storage import CSVStorage

app = Flask(__name__)
app.secret_key = "super_secret_key"

storage = JSONStorage()
DATA_FILE = "data.json"

def load_data():
    return storage.load(DATA_FILE)

def save_data(data):
    storage.save(data, DATA_FILE)

def get_current_user_profile():
    data = load_data()
    current_profile = data.get("current_profile", "Default")
    profiles_data = data.get("profiles", {})
    
    if current_profile not in profiles_data:
        profiles_data[current_profile] = {"currency": "PKR", "transactions": [], "budgets": {}, "goals": {}}
        
    user_data = profiles_data[current_profile]
    user = User(username=current_profile, currency=user_data.get("currency", "PKR"))
    
    for t_data in user_data.get("transactions", []):
        if t_data["type"] == "Income":
            user.add_transaction(Income(t_data["amount"], t_data["category"], t_data["date"], t_data["payment_type"]))
        else:
            user.add_transaction(Expense(t_data["amount"], t_data["category"], t_data["date"], t_data["payment_type"]))
            
    for cat, limit in user_data.get("budgets", {}).items():
        user.set_budget(cat, limit)
        
    for name, g_data in user_data.get("goals", {}).items():
        user.add_goal(Goal(name, g_data["target"], g_data["saved"]))
        
    return user, profiles_data, current_profile

def save_user_profile(user, profiles_data, current_profile):
    profiles_data[current_profile] = {
        "currency": user.currency,
        "transactions": [t.to_dict() for t in user.transactions],
        "budgets": {cat: b.limit for cat, b in user.budgets.items()},
        "goals": {g.name: {"target": g.target, "saved": g.saved} for g in user.goals}
    }
    data = {"current_profile": current_profile, "profiles": profiles_data}
    save_data(data)

@app.route("/")
def index():
    user, _, _ = get_current_user_profile()
    balance = user.get_balance()
    
    summary = {}
    for t in user.transactions:
        summary[t.category] = summary.get(t.category, 0) + t.apply()
        
    alerts = []
    for cat, budget in user.budgets.items():
        spent = sum(t.amount for t in user.transactions if isinstance(t, Expense) and t.category == cat)
        percentage = (spent / budget.limit) * 100 if budget.limit > 0 else 0
        if percentage >= 100:
            alerts.append(f"100% Limit reached for {cat}! (Spent: {spent}/{budget.limit})")
        elif percentage >= 80:
            alerts.append(f"80% limit crossed for {cat}! (Spent: {spent}/{budget.limit})")

    return render_template("dashboard.html", user=user, balance=balance, summary=summary, alerts=alerts)

@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    user, profiles_data, current_profile = get_current_user_profile()
    
    if request.method == "POST":
        t_type = request.form.get("type")
        amount = float(request.form.get("amount"))
        category = request.form.get("category")
        date = request.form.get("date")
        payment_type = request.form.get("payment_type")
        
        if t_type == "Income":
            user.add_transaction(Income(amount, category, date, payment_type))
        else:
            user.add_transaction(Expense(amount, category, date, payment_type))
            
        save_user_profile(user, profiles_data, current_profile)
        flash("Transaction added successfully!", "success")
        return redirect(url_for("index"))
        
    return render_template("add_transaction.html", currency=user.currency)

@app.route("/budgets_goals", methods=["GET", "POST"])
def budgets_goals():
    user, profiles_data, current_profile = get_current_user_profile()
    
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add_budget":
            cat = request.form.get("category")
            limit = float(request.form.get("limit"))
            user.set_budget(cat, limit)
            flash("Budget added!", "success")
        elif action == "add_goal":
            name = request.form.get("name")
            target = float(request.form.get("target"))
            saved = float(request.form.get("saved", 0))
            user.add_goal(Goal(name, target, saved))
            flash("Goal added!", "success")
            
        save_user_profile(user, profiles_data, current_profile)
        return redirect(url_for("budgets_goals"))

    budget_progress = {}
    for cat, budget in user.budgets.items():
        spent = sum(t.amount for t in user.transactions if isinstance(t, Expense) and t.category == cat)
        percentage = min((spent / budget.limit) * 100 if budget.limit > 0 else 0, 100)
        budget_progress[cat] = {"spent": spent, "limit": budget.limit, "percentage": round(percentage, 1)}
        
    return render_template("budgets_goals.html", budgets=budget_progress, goals=user.goals, currency=user.currency)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    data = load_data()
    profiles_data = data.get("profiles", {"Default": {}})
    current_profile = data.get("current_profile", "Default")
    
    if request.method == "POST":
        action = request.form.get("action")
        
        # New block for clearing data
        if action == "clear_data":
            if current_profile in profiles_data:
                profiles_data[current_profile]["transactions"] = []
                profiles_data[current_profile]["budgets"] = {}
                profiles_data[current_profile]["goals"] = {}
                save_data(data)
                flash(f"All data cleared for profile: {current_profile}", "success")
            return redirect(url_for("settings"))
            
        # Regular profile update block
        else:
            new_profile = request.form.get("profile_name")
            currency = request.form.get("currency")
            
            if new_profile and new_profile not in profiles_data:
                profiles_data[new_profile] = {"currency": currency, "transactions": [], "budgets": {}, "goals": {}}
            
            if new_profile:
                data["current_profile"] = new_profile
                profiles_data[new_profile]["currency"] = currency
                
            save_data(data)
            flash("Settings updated!", "success")
            return redirect(url_for("index"))
        
    return render_template("settings.html", profiles=profiles_data.keys(), current=current_profile)

if __name__ == "__main__":
    app.run(debug=True)