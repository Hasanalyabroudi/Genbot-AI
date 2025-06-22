import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";
import React, { useState } from 'react';
import HomePage from "./Pages/HomePage";
import ChatbotPage from "./Pages/ChatbotPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/chatbot" element={<ChatbotPage />} />
      </Routes>
    </Router>
  );
}

export default App;
