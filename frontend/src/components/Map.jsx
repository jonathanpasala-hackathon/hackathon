import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from "react-leaflet";
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';
import "./MapStyle.css";

// Fix default marker icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

export default function MapComponent({ eventMarkers = [], onLocationSelect }) {
    const [customMarkers, setCustomMarkers] = useState([]);

    // Filter valid event markers (must have lat & lng)
    const validEventMarkers = eventMarkers
        .filter(m => m.coords && typeof m.coords.lat === "number" && typeof m.coords.lng === "number")
        .map(m => ({ ...m.coords, title: m.title, isEvent: true }));

    // Filter valid custom markers
    const validCustomMarkers = customMarkers
        .filter(m => typeof m.lat === "number" && typeof m.lng === "number")
        .map(m => ({ ...m, isEvent: false }));

    // Combine markers
    const allMarkers = [...validEventMarkers, ...validCustomMarkers];

    // Map click handler
    function ClickHandler() {
        useMapEvents({
            click(e) {
                const newMarker = { lat: e.latlng.lat, lng: e.latlng.lng, isEvent: false };
                setCustomMarkers([...validCustomMarkers, newMarker]);
                if (onLocationSelect) onLocationSelect(newMarker);
            }
        });
        return null;
    }

    // Safe map center: first valid marker or default
    const mapCenter = allMarkers.length > 0
        ? [allMarkers[0].lat, allMarkers[0].lng]
        : [40.7128, -74.0060]; // default to New York

    return (
        <div className="map-wrapper">
            <MapContainer
                center={mapCenter}
                zoom={12}
                style={{ height: "400px", width: "100%" }}
            >
                <TileLayer
                    attribution='&copy; OpenStreetMap contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <ClickHandler />
                {allMarkers.map((marker, idx) => (
                    <Marker key={idx} position={[marker.lat, marker.lng]}>
                        {marker.isEvent && marker.title && <Popup>{marker.title}</Popup>}
                    </Marker>
                ))}
            </MapContainer>
        </div>
    );
}