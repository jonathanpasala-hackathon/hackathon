import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "./CalendarStyle.css";

export default function CalendarComponent({ selectedDate, setSelectedDate, events }) {

    // Filter events for selected date
    const filteredEvents = events.filter(event =>
        new Date(event.date).toDateString() === selectedDate.toDateString()
    );

    return (
        <div className="calendar-wrapper">
            <div className="calendar-container">
                <h2>Your Calendar</h2>
                <Calendar
                    onChange={setSelectedDate}
                    value={selectedDate}
                />
            </div>

            <div className="events-container">
                <h3>Events for {selectedDate.toDateString()}:</h3>
                {filteredEvents.length > 0 ? (
                    filteredEvents.map((event, index) => (
                        <div className="event-card" key={index}>
                            <p>{event.title}</p>
                        </div>
                    ))
                ) : (
                    <p className="no-events">No events for this day.</p>
                )}
            </div>
        </div>
    );
}