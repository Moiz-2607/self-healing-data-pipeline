import streamlit as st

from src.monitoring.health_summary import build_health_summary
from src.monitoring.recent_events import get_recent_events
from src.monitoring.event_counts import get_event_counts
from src.monitoring.risk_counts import get_risk_counts


st.set_page_config(
    page_title="Self-Healing Pipeline",
    page_icon="🔧",
    layout="wide",
)


st.title("🔧 Self-Healing Data Pipeline")
st.caption("Risk-aware data pipeline monitoring dashboard")


summary = build_health_summary()


st.subheader("Pipeline Health")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Events", summary["total_events"])

with col2:
    st.metric("Pipeline Successes", summary["pipeline_success"])

with col3:
    st.metric("Successful Repairs", summary["successful_repairs"])

with col4:
    st.metric("Rollbacks", summary["rollbacks"])


st.divider()

st.subheader("Human Review")

st.metric(
    "Review Required",
    summary["review_required"],
)


st.divider()

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Risk Distribution")

    risk_counts = get_risk_counts()

    if risk_counts:
        st.bar_chart(risk_counts)
    else:
        st.info("No risk-level data found.")


with chart_col2:
    st.subheader("Event Distribution")

    event_counts = get_event_counts()

    if event_counts:
        st.bar_chart(event_counts)
    else:
        st.info("No audit events found.")


st.divider()

st.subheader("Recent Incidents")

recent_events = get_recent_events(limit=10)

if recent_events:
    incident_rows = []

    for event in recent_events:
        details = event.get("details", {})

        incident_rows.append(
            {
                "Timestamp": event.get("timestamp", ""),
                "Event": event.get("event_type", ""),
                "Risk": details.get(
                    "risk_level",
                    details.get("risk", {}).get("risk_level", ""),
                ),
                "Status": details.get(
                    "final_status",
                    details.get("status", ""),
                ),
            }
        )

    st.dataframe(
        incident_rows,
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info("No audit events found.")


st.divider()

st.subheader("System Behavior")

st.write(
    """
The pipeline detects schema drift, classifies risk,
attempts safe recovery when appropriate, validates the
result, and rolls back failed repairs.
"""
)
