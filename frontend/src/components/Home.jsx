import CalendarComponent from "./Calendar";
import Chat from "./Chat";
import MapComponent from "./Map";
import Menu from "./Menu";
import { useState, useEffect } from "react";
import { processMessage, clearConversation } from "../services/api";
import "./HomeStyle.css";

export default function Home() {
    const [open, setOpen] = useState(false);
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [selectedCoords, setSelectedCoords] = useState(null);
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState([]);
    const [status, setStatus] = useState("");
    const [statusType, setStatusType] = useState("");
    const [loading, setLoading] = useState(false);
    const [displayData, setDisplayData] = useState([])

    useEffect(() => {
        console.log(displayData)
    }, [displayData])
    
    useEffect(() => {
    console.log("Chat mounted");
    return () => console.log("Chat unmounted");
    }, []);
    
    const addMessage = (text, sender, agent = null) => {
        setMessages((prev) => [
        ...prev,
        { text, sender, agent }
        ]);
    };
    const addDisplayData = (data) => {
        setDisplayData((prev) => [
            ...prev, ...data.filter(obj => obj && Object.keys(obj).length > 0)
        ])
    }
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;
    
        addMessage(input, "user");
        setInput("");
        setLoading(true);
        setStatus("Processing your request...");
        setStatusType("loading");
    
        try {
        const data = await processMessage(input);
    
        if (data.success) {
            addMessage(data.response, "assistant", data.agent);
            addDisplayData(data.display_data.data)
            setStatus("Request completed successfully");
            setStatusType("success");
        } else {
            addMessage(
            `Error: ${data.error || "Unknown error occurred"}`,
            "assistant"
            );
            setStatus("An error occurred");
            setStatusType("error");
        }
        } catch (err) {
        console.error(err);
        addMessage(
            "Sorry, there was an error processing your request.",
            "assistant"
        );
        setStatus("Connection error");
        setStatusType("error");
        } finally {
        setLoading(false);
        setTimeout(() => setStatus(""), 10000);
        }
    };    

    const handleClearConversation = async () => {
    try {
        await clearConversation();
        setMessages([{
        text: "Hello! How can I help you today?",
        sender: "assistant",
        agent: null
        }]);
        setStatus("Conversation cleared");
        setStatusType("success");
        setTimeout(() => setStatus(""), 2000);
    } catch (err) {
        console.error("Error clearing conversation:", err);
        setStatus("Failed to clear conversation");
        setStatusType("error");
        setTimeout(() => setStatus(""), 2000);
    }
    };

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
            <Menu open={open} openMenu={openMenu}/>
            <div className="home-page">
                <div className="left-panel">
                    <Chat 
                        messages={messages}
                        input={input}
                        setInput={setInput}
                        handleSubmit={handleSubmit}
                        handleClear={handleClearConversation}
                        status={status}
                        statusType={statusType}
                        loading={loading}
                    />
                </div>
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
        </div>
    );
}