import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

# ---------------- LOAD DATA ---------------- #

df = pd.read_csv("IPL2025Batters.csv")
numeric_cols = [
    "Runs",
    "AVG",
    "SR",
    "100s",
    "50s",
    "4s",
    "6s",
    "HS",
    "BF",
    "Inn",
    "NO"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("*", "", regex=False)
            .str.replace(",", "", regex=False)
        )

        df[col] = pd.to_numeric(df[col], errors="coerce")

df.fillna(0, inplace=True)
# ---------------- CSS ---------------- #

st.markdown("""
<style>

.main{
    background-color:#F5F5F5;
}

.title{
    text-align:center;
    font-size:48px;
    color:#E65100;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    font-size:20px;
    color:gray;
}

.player-card{
    background:#ffffff;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 0px 12px rgba(0,0,0,0.15);
}

</style>
""",unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.markdown("<h1 class='title'>🏏 IPL 2025 Analytics Dashboard</h1>",unsafe_allow_html=True)

st.markdown("<p class='subtitle'>Compare IPL Batters Like a Data Analyst</p>",unsafe_allow_html=True)

st.write("")

# ---------------- SIDEBAR ---------------- #

st.sidebar.header("Player Selection")

players = sorted(df["Player Name"].unique())

player1 = st.sidebar.selectbox(
    "Select Player 1",
    players,
    index=0
)

player2 = st.sidebar.selectbox(
    "Select Player 2",
    players,
    index=1
)

# ---------------- DATA ---------------- #

p1 = df[df["Player Name"] == player1].iloc[0]
p2 = df[df["Player Name"] == player2].iloc[0]

# ---------------- PLAYER CARDS ---------------- #

col1,col2 = st.columns(2)

with col1:

    st.subheader(player1)

    st.metric("Team",p1["Team"])

    st.metric("Runs",p1["Runs"])

    st.metric("Average",round(float(p1["AVG"]),2))

    st.metric("Strike Rate",round(float(p1["SR"]),2))

    st.metric("100s",p1["100s"])

    st.metric("50s",p1["50s"])

    st.metric("Fours",p1["4s"])

    st.metric("Sixes",p1["6s"])

with col2:

    st.subheader(player2)

    st.metric("Team",p2["Team"])

    st.metric("Runs",p2["Runs"])

    st.metric("Average",round(float(p2["AVG"]),2))

    st.metric("Strike Rate",round(float(p2["SR"]),2))

    st.metric("100s",p2["100s"])

    st.metric("50s",p2["50s"])

    st.metric("Fours",p2["4s"])

    st.metric("Sixes",p2["6s"])

st.divider()

# ---------------- COMPARISON TABLE ---------------- #

compare = pd.DataFrame({

    "Statistic":[
        "Runs",
        "Average",
        "Strike Rate",
        "100s",
        "50s",
        "Fours",
        "Sixes"
    ],

    player1:[
        p1["Runs"],
        p1["AVG"],
        p1["SR"],
        p1["100s"],
        p1["50s"],
        p1["4s"],
        p1["6s"]
    ],

    player2:[
        p2["Runs"],
        p2["AVG"],
        p2["SR"],
        p2["100s"],
        p2["50s"],
        p2["4s"],
        p2["6s"]
    ]

})

st.subheader("📊 Player Comparison")

st.dataframe(compare,use_container_width=True)

st.divider()

# ---------------- WINNER ---------------- #

stats = ["Runs","AVG","SR","100s","50s","4s","6s"]

score1 = 0
score2 = 0

for s in stats:

    if p1[s] > p2[s]:
        score1 += 1

    elif p2[s] > p1[s]:
        score2 += 1

st.subheader("🏆 Overall Winner")

if score1 > score2:

    st.success(f"🥇 {player1} wins!")

elif score2 > score1:

    st.success(f"🥇 {player2} wins!")

else:

    st.info("🤝 It's a Tie!")

# ---------------- PERFORMANCE ---------------- #

st.subheader("Performance Score")

progress1 = int((score1/7)*100)
progress2 = int((score2/7)*100)

st.write(player1)

st.progress(progress1)

st.write(f"{progress1}%")

st.write(player2)

st.progress(progress2)

st.write(f"{progress2}%")


# ============================================
# PART 2 STARTS HERE
# ============================================

st.divider()

st.header("🏆 Orange Cap Leaderboard")

orange = df.sort_values("Runs", ascending=False)

st.dataframe(
    orange[[
        "Player Name",
        "Team",
        "Runs",
        "AVG",
        "SR"
    ]].head(10),
    use_container_width=True
)
st.divider()
st.subheader("📊 Top 10 Run Scorers")


top_runs = df.sort_values("Runs", ascending=False).head(10)

fig = px.bar(
    top_runs,
    x="Player Name",
    y="Runs",
    color="Runs",
    text="Runs",
    title="Top 10 Run Scorers"
)

fig.update_layout(xaxis_title="Player")

st.plotly_chart(fig, use_container_width=True)



st.subheader("🚀 Highest Strike Rate")

top_sr = df.sort_values("SR", ascending=False).head(10)

fig = px.bar(
    top_sr,
    x="Player Name",
    y="SR",
    color="SR",
    text="SR"
)

st.plotly_chart(fig, use_container_width=True)




st.subheader("💥 Six Hitting Machine")

top6 = df.sort_values("6s", ascending=False).head(10)

fig = px.bar(
    top6,
    x="Player Name",
    y="6s",
    color="6s",
    text="6s"
)

st.plotly_chart(fig, use_container_width=True)




st.subheader("🔥 Most Boundaries")

df["Boundaries"] = df["4s"] + df["6s"]

boundary = df.sort_values(
    "Boundaries",
    ascending=False
).head(10)

fig = px.bar(
    boundary,
    x="Player Name",
    y="Boundaries",
    color="Boundaries",
    text="Boundaries"
)

st.plotly_chart(fig, use_container_width=True)








st.subheader("🏏 Team Runs")

team_runs = df.groupby("Team")["Runs"].sum().reset_index()

fig = px.pie(
    team_runs,
    names="Team",
    values="Runs",
    hole=.4
)

st.plotly_chart(fig, use_container_width=True)




st.subheader("📈 Team Average Runs")

fig = px.bar(
    team_runs.sort_values("Runs"),
    x="Team",
    y="Runs",
    color="Runs"
)

st.plotly_chart(fig, use_container_width=True)


st.divider()

st.header("🔎 Search Player")

search = st.text_input("Enter Player Name")

if search:

    result = df[
        df["Player Name"].str.contains(
            search,
            case=False
        )
    ]

    st.dataframe(result, use_container_width=True)




st.divider()

st.header("🕸 Player Radar Chart")

categories = [
    "Runs",
    "AVG",
    "SR",
    "100s",
    "50s",
    "4s",
    "6s"
]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(

    r=[
        p1["Runs"],
        p1["AVG"],
        p1["SR"],
        p1["100s"],
        p1["50s"],
        p1["4s"],
        p1["6s"]
    ],

    theta=categories,

    fill="toself",

    name=player1

))

fig.add_trace(go.Scatterpolar(

    r=[
        p2["Runs"],
        p2["AVG"],
        p2["SR"],
        p2["100s"],
        p2["50s"],
        p2["4s"],
        p2["6s"]
    ],

    theta=categories,

    fill="toself",

    name=player2

))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)    




st.divider()
st.header("⭐ Player Rating")

def player_rating(player):
    score = (
        player["Runs"] * 0.30 +
        player["AVG"] * 0.20 +
        player["SR"] * 0.20 +
        player["100s"] * 10 +
        player["50s"] * 5 +
        player["4s"] * 0.10 +
        player["6s"] * 0.20
    )
    return round(score, 2)

rating1 = player_rating(p1)
rating2 = player_rating(p2)

col1, col2 = st.columns(2)

with col1:
    st.metric(player1, rating1)

with col2:
    st.metric(player2, rating2)


st.divider()

report = f"""
IPL PLAYER REPORT

Player : {player1}

Team : {p1['Team']}

Runs : {p1['Runs']}

Average : {p1['AVG']}

Strike Rate : {p1['SR']}

100s : {p1['100s']}

50s : {p1['50s']}

4s : {p1['4s']}

6s : {p1['6s']}
"""

st.download_button(
    "⬇ Download Report",
    report,
    file_name=f"{player1}_Report.txt"
)    




st.divider()
st.header("🏆 MVP Leaderboard")

df["Player Rating"] = df.apply(player_rating, axis=1)

mvp = df.sort_values(
    "Player Rating",
    ascending=False
)

st.dataframe(
    mvp[
        ["Player Name",
         "Team",
         "Player Rating",
         "Runs",
         "AVG",
         "SR"]
    ].head(10),
    use_container_width=True
)




fig = px.bar(
    mvp.head(10),
    x="Player Name",
    y="Player Rating",
    color="Player Rating",
    text="Player Rating",
    title="Top Rated Players"
)

st.plotly_chart(fig, use_container_width=True)