
💰 Advanced Finance Tracker (Flask Web App)

A modern, fully functional **Personal Finance Tracking Web Application** built using **Python, Flask, SQLite, Chart.js, and custom CSS**.  
This app allows you to track income & expenses, visualize analytics, download CSV reports, and manage transactions through a clean UI.


⭐ Features

🔹 Dashboard Overview
- Total income, expense & balance
- Recent transactions
- Pie chart for category-wise expenses

🔹 Transaction Management
- Add income/expense
- Edit & delete entries
- Search transactions
- Custom categories & notes

🔹 Data & Reports
- SQLite storage
- Export to CSV
- Clean transaction table view

🔹 Frontend
- Responsive UI
- Custom CSS
- Chart.js visualizations


🏗️ Project Structure
```text
AdvancedFinanceWeb/
│
├── app.py                  # Main Flask application  
├── models.py               # Database models  
├── requirements.txt        # Dependencies  
├── README.md               # Documentation  
├── .gitignore  
│
├── templates/              # HTML templates  
│   ├── base.html  
│   ├── index.html  
│   ├── add.html  
│   ├── transactions.html  
│   └── edit.html  
│
└── static/  
    └── style.css           # Custom CSS styling  
```


⚙️ Installation & Setup

1. Clone the repository

```
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

2. Create a virtual environment

```
python -m venv venv
```

Activate:

Windows:
```
venv\Scripts\activate
```

macOS/Linux:
```
source venv/bin/activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Run the app

```
python app.py
```

Open in browser:
http://127.0.0.1:5000

---


🛠️ Tech Stack
```text
| Category | Tools |
|----------|--------|
| Backend | Flask, Python |
| Database | SQLite + SQLAlchemy |
| Frontend | HTML, CSS, JS |
| Charts | Chart.js |
| Export | Pandas |
```


🤝 Contributing
Pull requests are welcome!


⭐ Support
Please ⭐ the repository if you like this project!


