import os
import sys
import streamlit as st
from .content import tip1, tip2, tip3, tip4, tip5


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from apps import INFO_HEADER, INFO_FOOTER


def main():
    uuid = os.environ.get("AMPLKEY_UUID")
    if uuid is not None:
        from amplpy import modules

        modules.activate(uuid)

    tips = [(t.title, t.run) for t in [tip1, tip2, tip3, tip4, tip5]]
    tip_titles = [title for title, _ in tips]

    def update_params():
        st.experimental_set_query_params(
            tip=tip_titles.index(st.session_state.title) + 1
        )

    # Logo and Navigation
    _, col2, _ = st.columns((1, 4, 1))
    with col2:
        st.image("static/images/logo-inline-web-v4.png")
    st.markdown("# AMPL Modeling Tips")

    query_params = st.experimental_get_query_params()

    if query_params:
        if "tip" in query_params and query_params["tip"][0].isnumeric():
            tip = int(query_params["tip"][0])
            tip_index = min(max(tip, 1), len(tip_titles)) - 1
            st.session_state.title = tip_titles[tip_index]

    selected_tip = st.selectbox(
        "Pick the tip 👇", tip_titles, key="title", on_change=update_params
    )
    tip_index = tip_titles.index(selected_tip)

    # Sidebar
    st.sidebar.header("About")
    st.sidebar.markdown(INFO_HEADER)

    st.sidebar.header("Resources")
    st.sidebar.markdown(INFO_FOOTER)

    title, run = tips[tip_index]
    st.markdown(f"## 💡 {title}")
    run()