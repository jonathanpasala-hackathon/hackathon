import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";
import "./MapStyle.css";
import { useMap } from "react-leaflet";

// Fix default marker icon
delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
    iconRetinaUrl: markerIcon2x,
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
});

// Colored icons (hackathon-friendly)
const blueIcon = new L.Icon({
    iconUrl: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png",
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
});

const redIcon = new L.Icon({
    iconUrl: "https://maps.google.com/mapfiles/ms/icons/red-dot.png",
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
});

const yellowIcon = new L.Icon({
    iconUrl: "https://maps.google.com/mapfiles/ms/icons/yellow-dot.png",
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
});

export default function MapComponent({ eventMarkers = [], onLocationSelect, data = []}) {
    const [customMarker, setCustomMarker] = useState(null);

    // Calendar markers (blue)
    const validEventMarkers = eventMarkers
        .filter(
        (m) =>
            m.coords &&
            typeof m.coords.lat === "number" &&
            typeof m.coords.lng === "number"
        )
        .map((m) => ({ ...m.coords, title: m.title, markerType: "event" }));

    const validChatMarkers = data.filter(data => data.latitude != null && data.logitude != null).map(data => ({
        lat: Number(data.latitude),
        lng: Number(data.logitude),
        title: data.name,
        markerType: "chat"
    }))

    // User marker (red) - only one
    const validCustomMarker =
        customMarker &&
        typeof customMarker.lat === "number" &&
        typeof customMarker.lng === "number"
        ? { ...customMarker, markerType: "custom" }
        : null;

    const allMarkers = [
        ...validEventMarkers,
        ...validChatMarkers,
        ...(validCustomMarker ? [validCustomMarker] : []),
    ]

    function ClickHandler() {
        useMapEvents({
        click(e) {
            const newMarker = { lat: e.latlng.lat, lng: e.latlng.lng, isEvent: false };
            setCustomMarker(newMarker); // replaces previous
            if (onLocationSelect) onLocationSelect(newMarker);
        },
        });
        return null;
    }

    const mapCenter =
        validChatMarkers.length > 0 ? [validChatMarkers[0].lat, validChatMarkers[0].lng] :
        allMarkers.length > 0 ? [allMarkers[0].lat, allMarkers[0].lng] : [40.7128, -74.006];


    function RecenterMap({ center }) {
        const map = useMap();

        useEffect(() => {
            if (center) {
            map.setView(center, map.getZoom(), { animate: true });
            }
        }, [center, map]);

        return null;
    }

    return (
        <div className="map-wrapper">
        <MapContainer center={mapCenter} zoom={12} style={{ height: "400px", width: "100%" }}>
            <TileLayer
            attribution="&copy; OpenStreetMap contributors"
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            <ClickHandler />

            <RecenterMap center={mapCenter} />

            {allMarkers.map((marker, idx) => (
            <Marker
                key={idx}
                position={[marker.lat, marker.lng]}
                icon={marker.markerType == "event" ? blueIcon : marker.markerType == "chat" ? yellowIcon : redIcon}
                eventHandlers={
                marker.isEvent
                    ? undefined
                    : {
                        click: () => {
                        setCustomMarker(null); // remove only custom marker
                        if (onLocationSelect) onLocationSelect(null);
                        },
                    }
                }
            >
                {marker.isEvent && marker.title && <Popup>{marker.title}</Popup>}
                {!marker.isEvent && <Popup>Custom pin (click pin to remove)</Popup>}
            </Marker>
            ))}
        </MapContainer>
        </div>
    );
}
