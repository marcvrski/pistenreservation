import streamlit as st
import calendar
import re
from google.oauth2 import service_account
from google.cloud import bigquery
from streamlit_calendar import calendar
import pandas as pd

# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.title("Pistenreservation Zermatt Kalender")

# Setup for Panoply data collection
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

@st.cache_data(ttl='4h', show_spinner='Fetching new data...')
def load_panoply(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return pd.DataFrame(rows)

query = "SELECT * FROM `panoply.activities` WHERE club_id = 1"
df = load_panoply(query)
#st.write("Loaded data from Panoply:", df.head())

# Initialize session variables if they don't exist yet
if "current_view" not in st.session_state:
    st.session_state.current_view = "dayGridMonth"
if "calendar_refresh" not in st.session_state:
    st.session_state.calendar_refresh = 0
if "reset_view" not in st.session_state:
    st.session_state.reset_view = False

# Button to reset the view to overview
if st.button("Back to Overview"):
    st.session_state.reset_view = True

# Simulate a rerun by checking the reset flag and updating state
if st.session_state.reset_view:
    st.session_state.current_view = "dayGridMonth"
    st.session_state.calendar_refresh += 1  # update the refresh counter
    st.session_state.reset_view = False

# Create resources with an additional "order" property ensuring numerical order
resources = sorted(
    [{"id": f"p{i}", "piste": f"Piste {i}", "title": f"Piste {i}", "order": i} for i in range(1, 16)],
    key=lambda r: r["order"]
)

calendar_options = {
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
    },
    "slotMinTime": "06:00:00",
    "slotMaxTime": "18:00:00",
    "initialView": st.session_state.current_view,
    "initialDate": "2025-06-01",
    "resources": resources,
    "resourceOrder": "order",
}

# Function to convert each row in df into an event dictionary for the calendar.
def convert_row_to_event(row):
    event = {
        "title": row["activity_name"],
        # Ensure the start_date is in string format (e.g. "YYYY-MM-DD")
        "start": str(row["start_date"]),
        "allDay": True,
    }
    # Attempt to extract the piste number from the sub_location field (e.g., "Piste 01a (Speed)")
    resource = None
    if pd.notnull(row.get("sub_location")):
        match = re.search(r'Piste\s*(\d+)', row["sub_location"])
        if match:
            resource = f"p{int(match.group(1))}"
    event["resourceId"] = resource if resource else "p1"  # default resource if extraction fails
    return event

# Create calendar events list dynamically from the dataframe
calendar_events = df.apply(convert_row_to_event, axis=1).tolist()

custom_css = """
    .fc {
        margin-top: 0 !important;
    }
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
"""

# Use a dynamic key that combines current_view and the refresh counter
calendar_component = calendar(
    events=calendar_events,
    options=calendar_options,
    custom_css=custom_css,
    key=f'calendar-{st.session_state.current_view}-{st.session_state.calendar_refresh}',
)

# Optionally, display the events for debugging
#st.write("Calendar Events:", calendar_events)
