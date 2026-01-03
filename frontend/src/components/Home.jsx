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
        <span className="left-panel">
            <p>This is the left panel</p>
            <Chat />
        </span>
    );
}

function RightPanel() {
    return (
        <span className="right-panel">
            <p>This is the right panel</p>
        </span>
    );    
}