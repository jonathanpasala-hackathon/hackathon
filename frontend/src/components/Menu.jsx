import "./MenuStyle.css";
import questionMark from "../assets/questionMark.png";
import x from "../assets/x.svg";
import { useState } from "react";

export default function Menu({ open, openMenu }) {
    return (
        <div>
            <button className="menu-button" onClick={ openMenu }>
                {!open ? (
                    <img src={ questionMark } alt="It's a question mark?"/>
                ): (
                    <img src={ x } alt="It's a x"/>
                )}
            </button>

            {open && (
                <div className="menuPanel">
                    <p>This is the menu panel</p>
                </div>
            )}
        </div>
    );
}