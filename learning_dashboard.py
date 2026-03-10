import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

st.set_page_config(page_title="📚 Learning Dashboard", layout="wide")

# ── カスタムCSS ──────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(74,144,217,0.08);
        border-left: 4px solid #4A90D9;
    }
</style>
""", unsafe_allow_html=True)

# ── データ読み込み ────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("study_record.xlsx")
    df["日付"] = pd.to_datetime(df["日付"])
    df["週"] = df["日付"].dt.strftime("Week %U")
    df["累計Ankiカード"] = df["Ankiカード枚数"].cumsum()
    df["累計コマンド数"] = df["理解できたコマンド数"].cumsum()
    return df

df = load_data()

# ── タイトル ──────────────────────────────────────────
st.title("📚 Airiの学習ダッシュボード")
st.caption("Marketing Analytics Data Analyst への道のり")
st.divider()

# ── KPIカード ─────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("総学習時間", f"{df['学習時間（分）'].sum():,} 分")
k2.metric("学習日数", f"{len(df)} 日")
k3.metric("累計Ankiカード", f"{df['Ankiカード枚数'].sum()} 枚")
k4.metric("習得コマンド数", f"{df['理解できたコマンド数'].sum()} 個")

st.divider()

# ── グラフ行1 ─────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 日別学習時間")
    fig = px.line(df, x="日付", y="学習時間（分）",
                  markers=True, template="plotly_white",
                  labels={"日付": "日付", "学習時間（分）": "分"})
    fig.update_traces(line_color="#4A90D9", marker_size=10, marker_color="#4A90D9")
    fig.update_yaxes(range=[0, df["学習時間（分）"].max() * 1.3])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 週ごとの合計学習時間")
    weekly = df.groupby("週")["学習時間（分）"].sum().reset_index()
    weekly.columns = ["週", "合計学習時間（分）"]
    fig2 = px.bar(weekly, x="週", y="合計学習時間（分）",
                  color="合計学習時間（分）",
                  color_continuous_scale="Blues",
                  template="plotly_white")
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

# ── グラフ行2 ─────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("🃏 Ankiカード枚数の推移")
    fig3 = px.bar(df, x="日付", y="Ankiカード枚数",
                  template="plotly_white",
                  labels={"日付": "日付", "Ankiカード枚数": "枚数"},
                  color="Ankiカード枚数",
                  color_continuous_scale="Greens")
    fig3.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("💡 理解できたコマンド数の推移")
    fig4 = px.line(df, x="日付", y="累計コマンド数",
                   markers=True, template="plotly_white",
                   labels={"日付": "日付", "累計コマンド数": "累計コマンド数"})
    fig4.update_traces(line_color="#7BC8A4", marker_size=10, marker_color="#7BC8A4")
    fig4.add_bar(x=df["日付"], y=df["理解できたコマンド数"],
                 name="当日", marker_color="#E8F7F2")
    fig4.update_layout(showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── タグクラウド（学習内容） ────────────────────────────
st.subheader("🏷️ よく学んだトピック")
all_topics = []
for content in df["学習内容"].dropna():
    topics = [t.strip() for t in content.split(",")]
    all_topics.extend(topics)

topic_count = Counter(all_topics)

if topic_count:
    topic_df = pd.DataFrame(topic_count.items(), columns=["トピック", "回数"])
    topic_df = topic_df.sort_values("回数", ascending=False)
    fig5 = px.bar(topic_df, x="トピック", y="回数",
                  color="回数", color_continuous_scale="Oranges",
                  template="plotly_white")
    fig5.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig5, use_container_width=True)

# ── つまづいたトピック ──────────────────────────────────
st.subheader("🤔 つまづいたトピック一覧")
stumbled = []
for item in df["つまづいたトピック"].dropna():
    topics = [t.strip() for t in item.split(",")]
    stumbled.extend(topics)

stumbled_count = Counter(stumbled)
if stumbled_count:
    stumbled_df = pd.DataFrame(stumbled_count.items(), columns=["トピック", "回数"])
    stumbled_df = stumbled_df.sort_values("回数", ascending=False)
    fig6 = px.bar(stumbled_df, x="トピック", y="回数",
                  color="回数", color_continuous_scale="Reds",
                  template="plotly_white")
    fig6.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig6, use_container_width=True)

st.divider()

# ── 生データ ──────────────────────────────────────────
with st.expander("📋 生データを見る"):
    st.dataframe(df[["日付", "学習時間（分）", "学習内容", "Ankiカード枚数", "つまづいたトピック", "理解できたコマンド数"]])
