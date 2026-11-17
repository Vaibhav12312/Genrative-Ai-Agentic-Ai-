"""EPFOSathi Streamlit UI — chat, citations, feedback, and My PF timeline."""
from __future__ import annotations

import os
from datetime import date
from pathlib import Path
import streamlit as st

try:
    from api_client import call_backend, save_feedback
    from pf_timeline import build_pf_timeline
    from timeline_view import timeline_html
except ImportError:  # pragma: no cover
    from ui.api_client import call_backend, save_feedback
    from ui.pf_timeline import build_pf_timeline
    from ui.timeline_view import timeline_html

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "feedback.sqlite3"

def render_timeline(joining: date, exit_day: date | None) -> None:
    markers = build_pf_timeline(joining, exit_day)
    st.subheader("My PF timeline")
    st.caption("Indicative milestones calculated from the dates you enter. Confirm your service history and current EPFO/tax rules before acting.")
    st.markdown(timeline_html(joining, exit_day, markers, date.today()), unsafe_allow_html=True)
    for marker in markers:
        with st.expander(f"{marker.label} — {marker.when.strftime('%d %b %Y')}"):
            st.write(marker.detail)


def main() -> None:
    st.set_page_config(page_title="EPFOSathi", page_icon="🧾", layout="wide")
    st.title("🧾 EPFOSathi")
    st.caption("Your provident-fund companion · Ask questions, inspect sources, and map key PF milestones.")
    demo_mode = st.query_params.get("demo") == "1"
    if demo_mode:
        st.info("Demo mode: sample joining and exit dates are pre-filled for the Checkpoint 2 walkthrough. Answers come from the local mock backend.")

    with st.sidebar:
        st.header("Connection")
        env_url = os.getenv("EPFOSATHI_API_URL", "http://localhost:8000")
        base_url = st.text_input("Backend base URL", value=st.session_state.get("api_url", env_url), help="Base URL only; the app appends /ask or /agent.")
        st.session_state.api_url = base_url
        endpoint = st.radio("API route", ["ask", "agent"], horizontal=True, help="Calls POST /ask or POST /agent.")
        token = st.text_input("Bearer token (optional)", type="password", value=os.getenv("EPFOSATHI_API_TOKEN", ""))
        st.divider()
        st.caption("Feedback is stored locally in SQLite. Set EPFOSATHI_FEEDBACK_DB to change its location.")

    chat_col, timeline_col = st.columns([1.35, 1])
    with timeline_col:
        st.subheader("PF dates")
        # Outside the form: widgets inside st.form only update on submit, which would keep the exit date disabled.
        has_exit = st.checkbox("I have left this employment", value=demo_mode)
        with st.form("pf_dates"):
            joining = st.date_input("Date of joining", value=date(2020, 1, 1), max_value=date.today())
            exit_day = st.date_input("Date of exit", value=date(2024, 3, 10) if demo_mode else date.today(), max_value=date.today(), disabled=not has_exit)
            submitted = st.form_submit_button("Build my timeline", type="primary")
        if submitted:
            if has_exit and exit_day < joining:
                st.error("Exit date cannot be earlier than joining date.")
            else:
                st.session_state.pf_dates = (joining.isoformat(), exit_day.isoformat() if has_exit else None)
        if "pf_dates" not in st.session_state:
            st.session_state.pf_dates = (joining.isoformat(), None)
        saved_joining, saved_exit = st.session_state.pf_dates
        render_timeline(date.fromisoformat(saved_joining), date.fromisoformat(saved_exit) if saved_exit else None)

    with chat_col:
        st.subheader("Ask EPFOSathi")
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for index, item in enumerate(st.session_state.messages):
            with st.chat_message(item["role"]):
                st.markdown(item["content"])
                if item.get("citations"):
                    with st.expander("Sources / citations"):
                        for citation in item["citations"]:
                            if citation.get("url", "").startswith(("https://", "http://")):
                                st.markdown(f"- [{citation['label']}]({citation['url']})")
                            else:
                                st.markdown(f"- {citation['label']}")
                if item["role"] == "assistant" and item.get("question"):
                    voted = item.get("vote")
                    c1, c2, c3 = st.columns([1, 1, 8])
                    for col, vote, icon, tip in ((c1, "up", "👍", "Helpful"), (c2, "down", "👎", "Not helpful")):
                        with col:
                            if st.button(icon, key=f"{vote}_feedback_{index}", help=tip, disabled=voted is not None):
                                save_feedback(os.getenv("EPFOSATHI_FEEDBACK_DB", str(DEFAULT_DB)), item["question"], item["content"], vote)
                                item["vote"] = vote  # one vote per answer; buttons lock after saving
                                st.toast("Thanks — feedback saved.")
                                st.rerun()
                    if voted:
                        with c3:
                            st.caption(f"Feedback saved: {'👍' if voted == 'up' else '👎'}")

        prompt = st.chat_input("Ask about EPF, EPS, withdrawals, transfers, or tax…")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1] if not m.get("error")]
            with st.chat_message("assistant"):
                with st.spinner(f"Contacting /{endpoint}…"):
                    try:
                        answer, citations = call_backend(base_url, endpoint, prompt, history, token)
                        st.markdown(answer)
                        if citations:
                            with st.expander("Sources / citations", expanded=True):
                                for citation in citations:
                                    if citation.get("url", "").startswith(("https://", "http://")):
                                        st.markdown(f"- [{citation['label']}]({citation['url']})")
                                    else:
                                        st.markdown(f"- {citation['label']}")
                        st.session_state.messages.append({"role": "assistant", "content": answer, "citations": citations, "question": prompt})
                    except (ValueError, TypeError) as exc:
                        st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {exc}", "error": True})
                    except Exception as exc:
                        st.session_state.messages.append({"role": "assistant", "error": True, "content":
                            f"⚠️ Could not reach the EPFOSathi backend: {exc}\n\n"
                            "Check the base URL, API availability, authentication, and that the selected route exists."})
            # Rerun once so the newly appended assistant message gets its persistent feedback controls.
            st.rerun()

    st.divider()
    st.caption("EPFOSathi provides general information, not legal, tax, or EPFO adjudication. Dates are estimates; verify eligibility and current rules with EPFO or a qualified adviser.")


if __name__ == "__main__":
    main()
