import streamlit as st
from sentiment_analysis import analyze_sentiment

st.set_page_config(
    page_title="Employee Review Sentiment Analysis",
    page_icon="🏢",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.big-title {
    text-align:center;
    font-size:45px;
    font-weight:bold;
    color:white;
}

.subtitle {
    text-align:center;
    color:#A0A0A0;
    font-size:18px;
}

.metric-card {
    padding:20px;
    border-radius:10px;
    background-color:#1E293B;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📌 Project Information")

st.sidebar.info("""
Employee Review Sentiment Analysis

Features:
- Sentiment Rating (1-10)
- Review Summary
- Intelligent Suggestions
- Employee Feedback Insights
""")

# Header
st.markdown(
    "<div class='big-title'>🏢 Employee Review Sentiment Analysis</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Analyze employee reviews and generate insights</div>",
    unsafe_allow_html=True
)

st.divider()

review = st.text_area(
    "✍ Enter Employee Review",
    height=180
)

if st.button("🔍 Analyze Review", use_container_width=True):
    if review.strip() == "":
        st.error("Please enter a review.")
        st.stop()

    result = analyze_sentiment(review)

    rating = result["rating"]
    category = result["category"]

    st.subheader("📈 Analysis Result")
    st.caption(f"Review Length: {len(review.split())} words")

    # INVALID INPUT
    if rating is None:

        st.error("❌ Invalid Input Detected")

        st.metric(
            label="Status",
            value="Invalid Input"
        )

        st.subheader("📝 Summary")
        st.warning(result["summary"])

        if len(result["suggestions"]) > 0:
    
            st.subheader("💡 Suggestions")

            for suggestion in result["suggestions"]:
                 st.info(suggestion)

    else:

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="Sentiment Rating",
                value=f"{rating}/10"
            )

        with col2:

            if "Positive" in category:
                st.success(category)

            elif "Negative" in category:
                st.error(category)

            else:
                st.warning(category)

        score = int(((11 - rating) / 10) * 100)
        st.progress(score)

        st.subheader("📝 Summary")
        st.info(result["summary"])

        st.subheader("💡 Suggestions")

        for suggestion in result["suggestions"]:
            with st.expander(suggestion):
                st.write(suggestion)

        st.subheader("📊 Interpretation")

        if rating <= 2:
            st.success("Excellent employee feedback.")

        elif rating <= 4:
            st.success("Generally positive feedback.")

        elif rating == 5:
            st.warning("Neutral feedback.")

        elif rating <= 7:
            st.warning("Some areas need improvement.")

        else:
            st.error("Critical issues identified.")