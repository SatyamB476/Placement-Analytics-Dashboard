import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- Data Load ---
df = pd.read_csv("college_placement_data.csv")
df_original = df.copy()

# --- Sidebar Filters ---
st.sidebar.header("Filters")

selected_branch = st.sidebar.multiselect(
    "Select Branch",
    options=df["Branch"].unique(),
    default=df["Branch"].unique()
)

selected_year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=df["Year"].unique()
)

# Filter apply karo
df = df[
    (df["Branch"].isin(selected_branch)) &
    (df["Year"].isin(selected_year))
]

# --- Page Config ---
st.set_page_config(page_title="Placement Analytics", layout="wide")

# --- Title ---
st.title("College Placement Analytics Dashboard")
st.markdown("Analysis of 1500 students — placement trends, salary insights & more")

# --- Quick Stats ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", len(df))
col2.metric("Placed", df[df["PlacementStatus"]=="Placed"].shape[0])
col3.metric("Not Placed", df[df["PlacementStatus"]=="Not Placed"].shape[0])
col4.metric("Avg Salary", f"₹{df['Salary_INR'].mean():,.0f}")

st.divider()

# --- Level 1 : Overview ---
st.header("Overall Placement Overview")

col1, col2 = st.columns(2)

with col1:
    status_counts = df['PlacementStatus'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    fig1 = px.pie(status_counts,
                  values='Count',
                  names='Status',
                  title='Placement Status',
                  color_discrete_sequence=['#2ecc71', '#e74c3c'])
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    branch_placed = df[df['PlacementStatus']=='Placed'].groupby('Branch').size()
    branch_total = df.groupby('Branch').size()
    branch_rate = (branch_placed/branch_total*100).round(1).reset_index()
    branch_rate.columns = ['Branch', 'PlacementRate']
    fig2 = px.bar(branch_rate.sort_values('PlacementRate', ascending=False),
                  x='Branch', y='PlacementRate',
                  title='Placement Rate by Branch (%)',
                  color='PlacementRate',
                  color_continuous_scale='Greens',
                  text='PlacementRate')
    fig2.update_traces(texttemplate='%{text}%', textposition='outside')
    st.plotly_chart(fig2, use_container_width=True)
# ================================
# SECTION 2 — Factors
# ================================
st.divider()
st.header("Factors Affecting Placement")
col1,col2=st.columns(2)
with col1:                                           # CGPA box plot
    fig=px.box(df,x="PlacementStatus",y="CGPA",
    color="PlacementStatus",
    title='CGPA Distribution — Placed vs Not Placed')
    st.plotly_chart(fig, use_container_width=True)
with col2:                                           # Internships
    placed_student=df[df['PlacementStatus'] == 'Placed'].groupby("Internships").size()
    total_student=df.groupby("Internships").size()
    placementRate_intern=(placed_student/total_student *100).round(2).reset_index()
    placementRate_intern.columns=["Internships","PlacementRate"]
    fig=px.bar(placementRate_intern,x="Internships",
    y="PlacementRate",title="Placement Rate of Intern Student",
    color="PlacementRate")
    st.plotly_chart(fig,use_container_width=True)
col1, col2 = st.columns(2)
with col1:                       # Backlogs
    backlog_place=df[df["PlacementStatus"]=="Placed"].groupby("Backlogs").size()
    total_backlog=df.groupby("Backlogs").size()
    backlog_rate=(backlog_place/total_backlog *100).round(2).reset_index()
    backlog_rate.columns=["Backlogs","PlacementRate"]
    fig=px.bar(backlog_rate,x="Backlogs",y="PlacementRate",
    title="Backlogs % of Placed Student",
    color='PlacementRate',text="PlacementRate", 
    color_continuous_scale='Reds_r')
    st.plotly_chart(fig,use_container_width=True)
with col2:                       # Training
    Placed_train=df[df["PlacementStatus"]=="Placed"].groupby("PlacementTraining").size() 
    total_train=df.groupby("PlacementTraining").size()
    train_rate=(Placed_train/total_train *100).round(2).reset_index()
    train_rate.columns=["Placement_Training","training_Rate"]
    fig=px.bar(train_rate,x="Placement_Training",y="training_Rate",
    color="training_Rate",text="training_Rate",
    title="Placement Training Placed Rate")
    st.plotly_chart(fig,use_container_width=True)
# ================================
# SECTION 3 — Salary Analysis
# ================================
st.divider()
st.header("Salary Analysis")
col1, col2 = st.columns(2)
with col1:             # Branch avg salary
    Salary_Branch_Avg=df.groupby("Branch")["Salary_INR"].mean().round(2).reset_index()
    Salary_Branch_Avg.columns=["Branch","Salary_INR"]
    fig=px.bar(
        Salary_Branch_Avg,
        x="Branch",
        y="Salary_INR",
        color="Salary_INR",
        title="Average Salary by Branch"
    )
    st.plotly_chart(fig,use_container_width=True)
with col2:              # Company hiring
    total_company_hire=df.dropna(subset=["CompanyName"])
    total_company_hire=total_company_hire["CompanyName"].value_counts().reset_index()
    total_company_hire.columns=["CompanyName","StudentNo"]
    fig=px.bar(total_company_hire,x="CompanyName",y="StudentNo",
    text="StudentNo",color="StudentNo",
    title="No of Student Hired by Companies")
    st.plotly_chart(fig,use_container_width=True)

col1, col2 = st.columns(2)
with col1:                      # City salary
    avg_city_salary=df.dropna(subset=["Salary_INR"])
    avg_city_salary=avg_city_salary.groupby("JobCity")["Salary_INR"].mean().round(2).reset_index()
    avg_city_salary.columns=["JobCity","Salary_INR"]
    fig=px.bar(avg_city_salary,x="JobCity",y="Salary_INR",
    color="Salary_INR",title="Average salaries in Cities")
    st.plotly_chart(fig,use_container_width=True)
with col2:          # CGPA vs Salary
    Placed_Cgpa=df[df["PlacementStatus"]=="Placed"]
    fig=px.scatter(
        Placed_Cgpa,
        x="CGPA",
        y="Salary_INR",
        color="Branch",
        title="CGPA vs Salary — Placed Students"
    )
    st.plotly_chart(fig,use_container_width=True)
# ================================
# SECTION 4 — Combined Insights
# ================================
st.divider()
st.header("Combined Insights")
col1,col2=st.columns(2)
with col1:              # Communication vs Salary
    Salary_Com=df[df["PlacementStatus"]=="Placed"].dropna(subset=["Salary_INR"])
    fig=px.box(Salary_Com,x="CommunicationSkill",y="Salary_INR",
    color="CommunicationSkill",title="Communication Skill vs Salary",
    category_orders={"CommunicationSkill":["Poor","Average","Good","Excellent"]})
    st.plotly_chart(fig,use_container_width=True)
with col2:   # CGPA + Internships
    df["CGPA_Group"]=pd.cut(df["CGPA"],bins=[5.0,7.5,8.5,10],labels=["Low","Medium","High"])
    df=df.dropna(subset=["CGPA_Group"])
    placed=df[df["PlacementStatus"]=="Placed"].groupby(["CGPA_Group","Internships"]).size()
    total_std=df.groupby(["CGPA_Group","Internships"]).size()
    CGPA_Inter_Realtion=(placed/total_std*100).round(2).reset_index()
    CGPA_Inter_Realtion.columns=["Cgpa_Group","Internships","placeRate"]
    fig=px.bar(CGPA_Inter_Realtion,x="Cgpa_Group",
    color="Internships",y="placeRate", title="CGPA + Internships vs Placement_Rate",
    barmode="group",category_orders={"Cgpa_Group": ["Low","Medium","High"]})
    st.plotly_chart(fig,use_container_width=True)

# ================================
# SECTION 5 — AI Insights
# ================================
st.divider()
st.header("AI-Powered Insights")

from groq import Groq
client = Groq(api_key="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")

# Data summary banao
total = len(df)
placed = df[df["PlacementStatus"]=="Placed"].shape[0]
placement_rate = round(placed/total*100, 1)
top_branch = df[df["PlacementStatus"]=="Placed"].groupby("Branch").size().idxmax()
avg_salary = round(df["Salary_INR"].mean(), 0)
top_company = df.dropna(subset=["CompanyName"])["CompanyName"].value_counts().idxmax()

summary = f"""
Total Students: {total}
Placed: {placed} ({placement_rate}%)
Top Branch: {top_branch}
Average Salary: ₹{avg_salary:,.0f}
Top Hiring Company: {top_company}
"""

if st.button("Generate AI Insight"):
    with st.spinner("Analyzing data..."):
        response = client.chat.completions.create(
           model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"You are a data analyst. Analyze this placement data and give 3-4 key insights in simple English:\n{summary}"
            }]
        )
        st.success(response.choices[0].message.content)