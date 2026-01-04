import { useState } from "react";
import Chat from "./components/Chat";
import { processMessage } from "./services/api";
import Home from "./components/Home";

function App() {
  return (
    <Home/>
  );
}

export default App;