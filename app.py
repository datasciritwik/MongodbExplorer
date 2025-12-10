import streamlit as st
from pymongo import MongoClient
from bson.json_util import dumps
import json

st.set_page_config(page_title="MongoDB Explorer", layout="wide")

st.title("🔍 MongoDB Explorer (Custom Fast Client)")

# --- Enter connection URL ---
mongo_url = st.text_input("MongoDB Connection URI", type="password")

if mongo_url:
    try:
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=2000)
        client.server_info()  # Check connection

        st.success("Connected to MongoDB!")

        # --- Select Database ---
        db_list = client.list_database_names()
        db_name = st.selectbox("Select Database", db_list)

        if db_name:
            db = client[db_name]
            col_list = db.list_collection_names()

            # --- Select Collection ---
            col_name = st.selectbox("Select Collection", col_list)

            if col_name:
                col = db[col_name]

                # --- Query Inputs ---
                with st.expander("Advanced Query Options"):
                    query_raw = st.text_area("Filter (JSON)", "{}", height=100)
                    projection_raw = st.text_area("Projection (JSON)", "{}", height=100)
                    limit = st.number_input("Limit", min_value=1, max_value=500, value=50)
                    skip = st.number_input("Skip", min_value=0, value=0)

                try:
                    query = json.loads(query_raw)
                    projection = json.loads(projection_raw)

                    docs = list(col.find(query, projection).skip(skip).limit(limit))
                    st.write(f"Total Documents Shown: {len(docs)}")

                    st.json(json.loads(dumps(docs)))

                except Exception as e:
                    st.error(f"Query/Projection Error: {e}")

    except Exception as e:
        st.error(f"Connection failed: {e}")
