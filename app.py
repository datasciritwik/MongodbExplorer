import streamlit as st
from pymongo import MongoClient
from bson.json_util import dumps
import json

st.set_page_config(page_title="MongoDB Explorer", page_icon="🧭", layout="centered")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Configuration")

# Mongo URL input
mongo_url = st.sidebar.text_input("MongoDB Connection URI", type="password")

if mongo_url:
    try:
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=2000)
        client.server_info()
        st.sidebar.success("Connected")

        # DB selection
        st.sidebar.subheader("📂 Database")
        db_list = client.list_database_names()
        db_name = st.sidebar.selectbox("Select DB", db_list)

        if db_name:
            db = client[db_name]

            # Collection selection
            st.sidebar.subheader("📁 Collection")
            col_list = db.list_collection_names()
            col_name = st.sidebar.selectbox("Select Collection", col_list)

            if col_name:
                col = db[col_name]

                # Query options
                st.sidebar.subheader("🔎 Query Options")

                query_raw = st.sidebar.text_area("Filter (JSON)", "{}", height=120)
                projection_raw = st.sidebar.text_area("Projection (JSON)", "{}", height=120)

                limit = st.sidebar.number_input("Limit", min_value=1, value=50)
                skip = st.sidebar.number_input("Skip", min_value=0, value=0)

                run = st.sidebar.button("Run Query")

                if run:
                    try:
                        query = json.loads(query_raw)
                        projection = json.loads(projection_raw)

                        docs = list(col.find(query, projection).skip(skip).limit(limit))

                        # ---------------- MAIN OUTPUT ----------------
                        st.subheader(f"📄 Showing {len(docs)} Documents")

                        if not docs:
                            st.warning("No documents found.")
                        else:
                            # Show each document as collapsible block
                            for idx, doc in enumerate(docs):
                                with st.expander(f"📌 Document {idx+1} (ID: {doc.get('_id')})", expanded=False):
                                    st.code(
                                        json.dumps(json.loads(dumps(doc)), indent=4),
                                        language="json"
                                    )

                    except Exception as e:
                        st.error(f"Error executing query: {e}")

    except Exception as e:
        st.sidebar.error(f"Connection failed: {e}")

else:
    st.info("Enter a MongoDB connection URI in the sidebar.")

