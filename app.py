import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from agents.doc_agent import extract_from_pdf, process_document
from agents.news_agent import analyze_news
from agents.trend_agent import get_trend
from agents.decision_agent import generate_answer
from agents.planner_agent import plan_actions
from tools.ticker_mapper import get_ticker
from tools.memory_store import save_to_memory, get_recent_memories
from tools.pdf_export import export_to_pdf

st.set_page_config(page_title="FinSight – GenAI Financial Advisor", layout="centered")
st.title("📊 FinSight – Multi-Agent Financial Intelligence")

query = st.text_input("💬 Ask a financial question")
companies_input = st.text_input("🏢 Company Names (comma-separated)", placeholder="e.g. Infosys, TCS")
model = st.selectbox("🧠 LLM Model", ["phi3:instruct", "llama3", "mistral:instruct"])
temp = st.slider("🔧 Temperature", 0.0, 1.0, 0.7)
upload = st.file_uploader("📄 Upload financial PDF (optional)", type="pdf")

if st.button("🚀 Analyze") and query and companies_input:
    st.info("⏳ Running agents...")

    company_list = [c.strip() for c in companies_input.split(",") if c.strip()]
    plan = plan_actions(query)

    for company in company_list:
        st.subheader(f"📌 {company}")
        ticker = get_ticker(company)
        st.markdown(f"🆔 Detected Ticker: `{ticker}`")
        if not ticker:
            st.warning("❗ No ticker found.")
            continue

        news, sentiments, stock, doc_text = [], [], pd.DataFrame(), ""

        if plan["use_news_agent"]:
            news, sentiments = analyze_news(company)

        if plan["use_trend_agent"]:
            stock = get_trend(ticker)

        if plan["use_doc_agent"] and upload:
            doc_text = extract_from_pdf(upload)
            process_document(doc_text)

        answer = generate_answer(query, news, sentiments, stock.to_dict(), doc_text, model, temp)
        st.success("🧠 Answer:")
        st.markdown(answer)

        save_to_memory(query, answer, company)

        if st.button(f"📥 Export Answer for {company}"):
            pdf_path = export_to_pdf(company, query, answer)
            st.success(f"Saved PDF to: {pdf_path}")

        if not stock.empty and "Close" in stock.columns:
            st.markdown("📈 Stock Trend")
            stock = stock.reset_index()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=stock["Date"], y=stock["Close"], mode="lines+markers"))
            fig.update_layout(title=f"{company} Stock Trend", xaxis_title="Date", yaxis_title="Close")
            st.plotly_chart(fig)

        if sentiments:
            st.markdown("📰 News Sentiment")
            for s in sentiments:
                st.markdown(f"- **{s['sentiment']}**: {s['text'][:100]}...")

with st.expander("🧠 Past Interactions"):
    past = get_recent_memories()
    for mem in past:
        st.markdown(f"**Q:** {mem['question']}  \n**A:** {mem['answer'][:150]}...")
