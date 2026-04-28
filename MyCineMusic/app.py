import pandas as pd
import streamlit as st

from db import run_query, test_connection
from queries import QUERY_SPACE, QUERY_BY_KEY

st.set_page_config(page_title="MyCineMusic Distributed DB", page_icon="🎬", layout="wide")

st.title("🎬 MyCineMusic Distributed Database Query Interface")
st.caption("Streamlit client for the Docker/PostgreSQL distributed schema. Connect to the coordinator node and query reconstructed global views.")

with st.sidebar:
    st.header("Database connection")
    host = st.text_input("Host", value="localhost")
    port = st.number_input("Port", value=5432, min_value=1, max_value=65535)
    dbname = st.text_input("Database", value="mycinemusic")
    user = st.text_input("User", value="postgres")
    password = st.text_input("Password", value="postgres", type="password")
    conn_overrides = {"host": host, "port": int(port), "dbname": dbname, "user": user, "password": password}

    if st.button("Test connection"):
        try:
            st.success(test_connection(conn_overrides))
        except Exception as exc:
            st.error(f"Connection failed: {exc}")

st.subheader("Query space")
query_table = pd.DataFrame([
    {"Option": i + 1, "Query": q.title, "Category": q.category, "What it does": q.description}
    for i, q in enumerate(QUERY_SPACE)
])
st.dataframe(query_table, use_container_width=True, hide_index=True)

labels = {f"{i + 1}. {q.title}": q.key for i, q in enumerate(QUERY_SPACE)}
selected_label = st.selectbox("Choose a query", options=list(labels.keys()))
query = QUERY_BY_KEY[labels[selected_label]]

st.markdown(f"### {query.title}")
st.info(query.description)

with st.form(key=f"form_{query.key}"):
    cols = st.columns(2)
    values = {}
    for idx, spec in enumerate(query.params):
        target = cols[idx % 2]
        with target:
            name = spec["name"]
            ptype = spec["type"]
            if ptype == "select":
                default = spec.get("default", spec["options"][0])
                index = spec["options"].index(default) if default in spec["options"] else 0
                values[name] = st.selectbox(spec["label"], spec["options"], index=index, key=f"{query.key}_{name}")
            elif ptype == "number":
                values[name] = st.number_input(
                    spec["label"],
                    value=spec.get("default", 0),
                    min_value=spec.get("min", 0),
                    max_value=spec.get("max", 1000000000),
                    step=1,
                    key=f"{query.key}_{name}",
                )
            else:
                values[name] = st.text_input(spec["label"], value=spec.get("default", ""), key=f"{query.key}_{name}")

    run_button = st.form_submit_button("Run query")

if run_button:
    try:
        df = run_query(query.sql, values, conn_overrides)
        st.success(f"Returned {len(df)} row(s).")
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download results as CSV", csv, file_name=f"{query.key}.csv", mime="text/csv")
        with st.expander("SQL used"):
            st.code(query.sql, language="sql")
            st.json(values)
    except Exception as exc:
        st.error(f"Query failed: {exc}")
        st.caption("Check that Docker is running, the coordinator is healthy, and the schema was initialized.")

with st.expander("How to run"):
    st.code(
        """
# 1) Start the distributed DB from the SQL package directory
cd mycinemusic_distributed_db
docker compose up -d

# 2) Install and launch this Streamlit app
cd ../mycinemusic_streamlit_app
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
        """.strip(),
        language="bash",
    )
