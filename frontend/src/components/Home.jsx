import CalendarComponent from "./Calendar";
import Chat from "./Chat";
import MapComponent from "./Map";
import Menu from "./Menu";
import { useState } from "react";
import "./HomeStyle.css";

export default function Home() {
    const [open, setOpen] = useState(false);
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [selectedCoords, setSelectedCoords] = useState(null);

    const openMenu = () => setOpen(!open);

    // All events with coordinates
    const events = [
        { date: "2026-01-03", title: "Team Meeting", coords: { lat: 40.7128, lng: -74.0060 } },
        { date: "2026-01-03", title: "Lunch with Sarah", coords: { lat: 40.73061, lng: -73.935242 } },
        { date: "2026-01-04", title: "Project Deadline", coords: { lat: 40.758896, lng: -73.985130 } },
        { date: "2026-01-05", title: "Gym Session", coords: { lat: 40.741895, lng: -73.989308 } },
    ];

    // Markers for map: only events on the selected date
    const eventMarkers = events.filter(e => new Date(e.date).toDateString() === selectedDate.toDateString());

    return (
        <div className="app-row">
            <Menu open={open} openMenu={openMenu} />
            {!open && (
                <div className="home-page">
                    <div className="left-panel"><Chat /></div>
                    <div className="right-panel">
                        <CalendarComponent
                            selectedDate={selectedDate}
                            setSelectedDate={setSelectedDate}
                            events={events}
                        />
                        <MapComponent
                            eventMarkers={eventMarkers}
                            onLocationSelect={setSelectedCoords}
                        />
                        {selectedCoords && (
                            <p>
                                Selected coordinates: <strong>Lat:</strong> {selectedCoords.lat.toFixed(5)}, <strong>Lng:</strong> {selectedCoords.lng.toFixed(5)}
                            </p>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}