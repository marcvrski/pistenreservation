import streamlit as st
import calendar
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

# Initialize session variables
if "current_view" not in st.session_state:
    st.session_state.current_view = "dayGridMonth"

if "calendar_refresh" not in st.session_state:
    st.session_state.calendar_refresh = 0

# Button to reset the view to overview
if st.button("Back to Overview"):
    st.session_state.current_view = "dayGridMonth"
    st.session_state.calendar_refresh += 1  # update the refresh counter
    st.experimental_rerun()  # Force the app to re-run, updating the calendar view

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
    "initialView": st.session_state.current_view,  # Use dynamic view
    "initialDate": "2025-06-01",  # Start with June 2025
    "resources": resources,
    "resourceOrder": "order",  # This explicitly orders the resources based on the "order" property
}

# Define event data in a structured format
data = [
    {"title": "SwissSki Mastery F", "start": "2025-06-01", "allDay": True, "resourceId": "p10", "color": "red"},
    {"title": "SwissSki Mastery F", "start": "2025-06-02", "allDay": True, "resourceId": "p12", "color": "red"},
    {"title": "SwissSki Mastery F", "start": "2025-06-03", "allDay": True, "resourceId": "p8", "color": "red"},
    {"title": "SwissSki Mastery M", "start": "2025-06-04", "allDay": True, "resourceId": "p1"},
    {"title": "NLZ Ost", "start": "2025-06-05", "allDay": True, "resourceId": "p2"},
    {"title": "SwissSki Mastery F", "start": "2025-06-06", "allDay": True, "resourceId": "p1", "color": "red"},
    {"title": "NLZ Mitte", "start": "2025-06-07", "allDay": True, "resourceId": "p12", "color": "green"},
    {"title": "NLZ West", "start": "2025-06-08", "allDay": True, "resourceId": "p5", "color": "orange"},
    {"title": "International", "start": "2025-06-09", "allDay": True, "resourceId": "p9", "color": "grey"},

    {"title": "SwissSki Mastery F", "start": "2025-06-11", "allDay": True, "resourceId": "p10", "color": "red"},
    {"title": "SwissSki Mastery F", "start": "2025-06-12", "allDay": True, "resourceId": "p12", "color": "red"},
    {"title": "SwissSki Mastery F", "start": "2025-06-13", "allDay": True, "resourceId": "p8", "color": "red"},
    {"title": "SwissSki Mastery M", "start": "2025-06-14", "allDay": True, "resourceId": "p1"},
    {"title": "NLZ Ost", "start": "2025-06-15", "allDay": True, "resourceId": "p2"},
    {"title": "SwissSki Mastery F", "start": "2025-06-16", "allDay": True, "resourceId": "p1", "color": "red"},
    {"title": "NLZ Mitte", "start": "2025-06-17", "allDay": True, "resourceId": "p12", "color": "green"},
    {"title": "NLZ West", "start": "2025-06-18", "allDay": True, "resourceId": "p5", "color": "orange"},
    {"title": "International", "start": "2025-06-19", "allDay": True, "resourceId": "p9", "color": "grey"},

    {"title": "SwissSki Mastery F", "start": "2025-06-21", "allDay": True, "resourceId": "p10", "color": "red"},
    {"title": "SwissSki Mastery F", "start": "2025-06-22", "allDay": True, "resourceId": "p12", "color": "red"},
    {"title": "SwissSki Mastery F", "start": "2025-06-23", "allDay": True, "resourceId": "p8", "color": "red"},
    {"title": "SwissSki Mastery M", "start": "2025-06-24", "allDay": True, "resourceId": "p1"},
    {"title": "NLZ Ost", "start": "2025-06-25", "allDay": True, "resourceId": "p2"},
    {"title": "SwissSki Mastery F", "start": "2025-06-26", "allDay": True, "resourceId": "p1", "color": "red"},
    {"title": "NLZ Mitte", "start": "2025-06-27", "allDay": True, "resourceId": "p12", "color": "green"},
    {"title": "NLZ West", "start": "2025-06-28", "allDay": True, "resourceId": "p5", "color": "orange"},
    {"title": "International", "start": "2025-06-29", "allDay": True, "resourceId": "p9", "color": "grey"},

    {"title": "SwissSki Mastery F", "start": "2025-06-30", "allDay": True, "resourceId": "p10", "color": "red"},
    {"title": "SwissSki Mastery F", "start": "2025-06-27", "allDay": True, "resourceId": "p12", "color": "red"},
    {"title": "SwissSki Mastery F", "start": "2025-06-26", "allDay": True, "resourceId": "p8", "color": "red"},
    {"title": "SwissSki Mastery M", "start": "2025-06-25", "allDay": True, "resourceId": "p1"},
    {"title": "NLZ Ost", "start": "2025-06-24", "allDay": True, "resourceId": "p2"},
    {"title": "SwissSki Mastery F", "start": "2025-06-23", "allDay": True, "resourceId": "p1", "color": "red"},
    {"title": "NLZ Mitte", "start": "2025-06-22", "allDay": True, "resourceId": "p12", "color": "green"},
    {"title": "NLZ West", "start": "2025-06-21", "allDay": True, "resourceId": "p5", "color": "orange"},
    {"title": "International", "start": "2025-06-20", "allDay": True, "resourceId": "p9", "color": "grey"},
]

# Create a DataFrame for better organization
events_df = pd.DataFrame(data)
events_df = events_df.where(pd.notnull(events_df), None)

# Convert DataFrame to list of dictionaries expected by the calendar component
calendar_events = events_df.to_dict(orient="records")

custom_css = """
    .fc {
        margin-top: 0 !important;  /* Remove top margin */
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
#st.write(calendar_component)
