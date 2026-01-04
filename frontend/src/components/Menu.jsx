import "./MenuStyle.css";
import questionMark from "../assets/questionMark.png";
import x from "../assets/x.svg";
import { useState } from "react";

export default function Menu({ open, openMenu }) {
    return (
        <div>
            <button className="menu-button" onClick={ openMenu } type="button">
                {!open ? (
                    <img src={ questionMark } alt="It's a question mark?"/>
                ): (
                    <img src={ x } alt="It's a x"/>
                )}
            </button>

            {/* Backdrop only when open */}
      {open && <div className="menuBackdrop" onClick={openMenu} />}

      {/* Sidebar always exists; class controls animation */}
      <div className={`menuPanel ${open ? "open" : ""}`}>
        <div className="menuHeader">
            <button
                className="menu-button menuClose"
                onClick={openMenu}
                type="button"
            >
                <img src={x} alt="Close" />
            </button>
        </div>

        <div className="menuBody">
            <h className="menu-header">Description</h>
          <div className="agentBubble">
            <h4>Reservation & Booking</h4>
            <p>Finds restaurants/hotels and helps book reservations based on your preferences.</p>
        </div>

        <div className="agentBubble">
            <h4>Trip Planning</h4>
            <p>Builds trip itineraries, suggests flights/hotels, and organizes plans for your schedule.</p>
        </div>

        <div className="agentBubble">
            <h4>QA</h4>
            <p>Answers questions, explains steps, and helps troubleshoot or clarify tasks.</p>
        </div>
        </div>
      </div>
    </div>
  );
}