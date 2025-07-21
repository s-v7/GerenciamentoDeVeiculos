import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          path="/dashboard"
          element={<h1 className="text-white">DASHBOARD (em breve)</h1>}
        />
      </Routes>
    </Router>
  );
}

export default App;
