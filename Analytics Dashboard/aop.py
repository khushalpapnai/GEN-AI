import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

st.set_page_config(page_title="CSV Analytics Dashboard", layout="wide")
st.title("CSV Analytics Dashboard")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

def load_example():
    return sns.load_dataset("titanic")

if st.button("Use example dataset"):
    df = load_example()
    st.success("Example dataset loaded")
else:
    df = None

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception:
        st.error("Failed to read CSV file")
        df = None

if df is not None:
    st.subheader("Preview")
    st.dataframe(df.head(100))

    st.subheader("Summary Statistics")
    st.dataframe(df.describe(include="all").transpose())

    st.subheader("Missing values per column")
    miss = df.isnull().sum()
    miss_df = miss[miss > 0].sort_values(ascending=False)
    if not miss_df.empty:
        st.bar_chart(miss_df)
    else:
        st.write("No missing values detected")

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    if numeric_cols:
        st.subheader("Numeric charts")
        col1, col2 = st.columns([1,1])
        with col1:
            hist_col = st.selectbox("Histogram column", numeric_cols)
            fig_hist = px.histogram(df, x=hist_col, nbins=30, title=f"Histogram of {hist_col}")
            st.plotly_chart(fig_hist, use_container_width=True)
        with col2:
            x_col = st.selectbox("Scatter X", numeric_cols, index=0)
            y_col = st.selectbox("Scatter Y", numeric_cols, index=1 if len(numeric_cols)>1 else 0)
            fig_scatter = px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}", marginal_x="histogram", marginal_y="histogram")
            st.plotly_chart(fig_scatter, use_container_width=True)

    if cat_cols and numeric_cols:
        st.subheader("Group summary")
        group_col = st.selectbox("Group by", cat_cols)
        agg_col = st.selectbox("Aggregate numeric column", numeric_cols)
        summary = df.groupby(group_col)[agg_col].agg(["count", "mean", "sum"]).reset_index()
        st.dataframe(summary.sort_values(by="count", ascending=False).head(100))
        fig_bar = px.bar(summary, x=group_col, y="mean", title=f"Mean {agg_col} by {group_col}")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Simple cleaning")
    na_pct = (df.isnull().sum() / len(df)) * 100
    st.dataframe(na_pct[na_pct > 0].sort_values(ascending=False).to_frame("missing_pct"))
    drop_threshold = st.slider("Drop columns with missing percentage greater than", 0, 100, 90)
    keep_cols = [c for c in df.columns if (df[c].isnull().mean() * 100) <= drop_threshold]
    cleaned = df[keep_cols].copy()
    st.write("Kept columns:", len(keep_cols))
    st.dataframe(cleaned.head())

    st.subheader("Download cleaned CSV")
    csv = cleaned.to_csv(index=False).encode("utf-8")
    st.download_button(label="Download cleaned CSV", data=csv, file_name="cleaned.csv", mime="text/csv")

else:
    st.info("Upload a CSV file or click Use example dataset to get started")
