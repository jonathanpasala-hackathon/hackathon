import Chat from "./Chat";
import "./HomeStyle.css";
import Menu from "./Menu";
import { useState } from "react";

export default function Home(props) {
    const [open, setOpen] = useState(false);
    const openMenu = () => setOpen(!open);

    return (
        <div className="app-row">
            <Menu
                open = {open}
                openMenu = {openMenu}
            />
            {!open && (
                <div className="home-page">
                    <LeftPanel/>
                    <RightPanel/>
                </div>
            )}
        </div>
    );
}

function LeftPanel() {
    return (
        <div className="left-panel">
            <Chat />
        </div>
    );
}

function RightPanel() {
    return (
        <span className="right-panel">
            <p>This is the right panel</p>
        </span>
    );    
}