import streamlit as st
import calendar
from streamlit_calendar import calendar

st.title("Pistenreservation Zermatt Kalendar")

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
    "initialView": "resourceTimelineDay",
    "resources": resources,
    "resourceOrder": "order",  # This explicitly orders the resources based on the "order" property
}

calendar_events = [
    {
        "title": "Event 1",
        "start": "2023-07-31T08:30:00",
        "end": "2023-07-31T10:30:00",
        "resourceId": "p1",
    },
    {
        "title": "Event 2",
        "start": "2023-07-31T07:30:00",
        "end": "2023-07-31T10:30:00",
        "resourceId": "p2",
    },
    {
        "title": "Event 3",
        "start": "2023-07-31T10:40:00",
        "end": "2023-07-31T12:30:00",
        "resourceId": "p1",
    }
]

custom_css = """
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

calendar_component = calendar(
    events=calendar_events,
    options=calendar_options,
    custom_css=custom_css,
    key='calendar',  # Assign a widget key to prevent state loss
)
st.write(calendar_component)
