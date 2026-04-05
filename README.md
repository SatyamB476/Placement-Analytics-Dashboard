# 📊 College Placement Analytics Dashboard

> An AI-powered interactive dashboard that analyzes placement trends, salary insights, and key factors affecting student placement outcomes — built with Python, Plotly, and Streamlit.

---

## 🔴 Live Demo
> https://placement-analytics-dashboard-medfzmsbpyva2rf7oaqinu.streamlit.app/

---

## 📌 Project Overview

This dashboard analyzes placement data of **1,500 students** across 7 engineering branches and 4 academic years. It provides interactive visualizations and AI-generated insights to understand what factors drive placement success.

---

## ✨ Features

- **Overview Analysis** — Placement rate by branch, gender-wise breakdown
- **Factor Analysis** — Impact of CGPA, internships, backlogs, and placement training
- **Salary Insights** — Average salary by branch, company, and city
- **Combined Insights** — CGPA + internships combined effect, communication skill vs salary
- **AI-Powered Summary** — One-click AI insights generated using Groq LLaMA 3.3
- **Interactive Filters** — Filter all charts by branch and year in real-time

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Pandas | Data manipulation |
| Plotly | Interactive visualizations |
| Streamlit | Web dashboard |
| Groq API (LLaMA 3.3) | AI-generated insights |
| python-dotenv | Secure API key management |

---

## 📁 Project Structure

```
Placement-Analytics-Dashboard/
│
├── app.py                        # Streamlit dashboard
├── main.ipynb                    # Exploratory data analysis
├── college_placement_data.csv    # Dataset (1500 students)
├── .gitignore                    # Ignores .env file
├── requirements.txt              # Dependencies
└── README.md                     # Project documentation
```

---

## 🚀 How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/SatyamB476/Placement-Analytics-Dashboard.git
cd Placement-Analytics-Dashboard
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up your API key**

Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free API key at [console.groq.com](https://console.groq.com)

**4. Run the dashboard**
```bash
streamlit run app.py
```

---

## 📊 Dashboard Sections

| Section | Charts |
|---------|--------|
| Overview | Placement status pie, Branch-wise placement rate |
| Factors | CGPA box plot, Internships bar, Backlogs bar, Training effect |
| Salary | Branch salary, Company hiring, City salary, CGPA vs Salary scatter |
| Combined | Communication vs Salary, CGPA + Internships combined |
| AI Insights | LLaMA-powered data summary |

---

## 🤖 AI Insights Feature

Click the **"Generate AI Insight"** button to get 3-4 key insights from the current filtered data — powered by **Groq's LLaMA 3.3 70B** model.

---

## 👤 Author

**Satyam** — Final Year CS Student  
[GitHub](https://github.com/SatyamB476)

---

> Built as a portfolio project demonstrating Python data analytics + AI integration skills.
