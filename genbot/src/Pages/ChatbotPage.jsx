import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import CompanyCards from '../components/CompanyCard';
import { FiMessageSquare as MessageSquare } from 'react-icons/fi';
import { Button } from '../components/Button';

// Helper function to clean a raw database name.
// For example: "www_consulatdumaroc_ca_db" -> "consulatdumaroc.ca"
const cleanDatabaseName = (rawName) => {
  let name = rawName.replace(/^www_/, '');
  const match = name.match(/_(ca|com)_db$/);
  if (match) {
    const tld = match[1];
    name = name.replace(/_(ca|com)_db$/, '');
    name = name + '.' + tld;
  } else {
    name = name.replace(/_db$/, '');
  }
  return name;
};

// Custom component that renders HTML content and ensures all links open in a new tab.
const BotMessage = ({ htmlContent }) => {
  const messageRef = useRef(null);

  useEffect(() => {
    if (messageRef.current) {
      const links = messageRef.current.querySelectorAll('a');
      links.forEach(link => {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
      });
    }
  }, [htmlContent]);

  return <div ref={messageRef} dangerouslySetInnerHTML={{ __html: htmlContent }} />;
};

const ChatbotPage = () => {
  const navigate = useNavigate();
  const messagesEndRef = useRef(null);

  const [selectedDatabase, setSelectedDatabase] = useState(null);
  const [chatMessages, setChatMessages] = useState({});
  const [currentMessage, setCurrentMessage] = useState('');
  const [showAdminLogin, setShowAdminLogin] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [scrapedPages, setScrapedPages] = useState(0);
  const [availableDatabases, setAvailableDatabases] = useState([]);
  const [isAdmin, setIsAdmin] = useState(false);
  const [loginHover, setLoginHover] = useState(false);
  const [inputButtonHover, setInputButtonHover] = useState(false);
  const [chatbotSettings, setChatbotSettings] = useState({});

  // New state to track if the bot is typing
  const [isBotTyping, setIsBotTyping] = useState(false);

  useEffect(() => {
    async function fetchDatabases() {
      try {
        const response = await fetch("http://52.188.193.108:8000/databases");
        const data = await response.json();
        setAvailableDatabases(data.databases);
      } catch (error) {
        console.error("Error fetching databases:", error);
      }
    }
    fetchDatabases();
  }, []);

  // Function to scroll to the bottom of the chat area
  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Automatically scroll whenever chatMessages, isBotTyping, or selectedDatabase changes
  useEffect(() => {
    scrollToBottom();
  }, [chatMessages, isBotTyping, selectedDatabase]);

  const dbMappingDisplay = availableDatabases.reduce((acc, db) => {
    acc[cleanDatabaseName(db)] = db;
    return acc;
  }, {});
  const displayDatabases = availableDatabases.map(db => cleanDatabaseName(db));

  const handleDatabaseSelect = (displayName) => {
    const rawDb = dbMappingDisplay[displayName];
    setSelectedDatabase(rawDb);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();

    // Prevent sending a new message while the bot is still typing
    if (isBotTyping) return;
    if (!currentMessage.trim() || !selectedDatabase) return;

    // Add user message
    setChatMessages(prev => ({
      ...prev,
      [selectedDatabase]: [
        ...(prev[selectedDatabase] || []),
        { sender: 'user', text: currentMessage }
      ]
    }));

    const messageQuery = currentMessage;
    setCurrentMessage('');

    const db = selectedDatabase;
    if (!db || (availableDatabases.length > 0 && !availableDatabases.includes(db))) {
      const errorReply = "Database not available for this company.";
      setChatMessages(prev => ({
        ...prev,
        [selectedDatabase]: [
          ...(prev[selectedDatabase] || []),
          { sender: 'bot', text: errorReply }
        ]
      }));
      return;
    }

    // Show loading indicator
    setIsBotTyping(true);

    try {
      const url = `http://52.188.193.108:8000/generate_response/db=${db}/query=${encodeURIComponent(messageQuery)}`;
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      setChatMessages(prev => ({
        ...prev,
        [selectedDatabase]: [
          ...(prev[selectedDatabase] || []),
          { sender: 'bot', text: <BotMessage htmlContent={data.reply} /> }
        ]
      }));
    } catch (error) {
      console.error("Error generating response:", error);
      setChatMessages(prev => ({
        ...prev,
        [selectedDatabase]: [
          ...(prev[selectedDatabase] || []),
          { sender: 'bot', text: "Error generating response." }
        ]
      }));
    } finally {
      // Hide the loading indicator once response is processed
      setIsBotTyping(false);
    }
  };

  const handleAdminLogin = (e) => {
    e.preventDefault();
    if (username === 'admin' && password === 'admin') {
      setIsAdmin(true);
      setUsername('');
      setPassword('');
      setShowAdminLogin(false);
    } else {
      alert('Invalid credentials');
    }
    setLoginHover(false);
  };

  const handleSaveSettings = (newSettings) => {
    const displayName = selectedDatabase ? cleanDatabaseName(selectedDatabase) : null;
    if (displayName) {
      setChatbotSettings(prev => ({
        ...prev,
        [displayName]: newSettings,
      }));
    }
  };

  if (showAdminLogin) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', backgroundColor: '#f7fafc' }}>
        <div style={{ width: '100%', maxWidth: '28rem', padding: '32px', display: 'flex', flexDirection: 'column', gap: '32px', backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05)' }}>
          <div style={{ textAlign: 'center' }}>
            <h1 style={{ fontSize: '1.5rem', fontWeight: '700', color: '#4338CA' }}>Admin Login</h1>
            <p style={{ marginTop: '8px', color: '#4a5568' }}>Sign in to access admin controls</p>
          </div>
          <form onSubmit={handleAdminLogin} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div>
                <label htmlFor="username" style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#4a5568' }}>Username</label>
                <input
                  id="username"
                  name="username"
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  style={{ width: '100%', padding: '8px 12px', marginTop: '4px', border: '1px solid #e2e8f0', borderRadius: '4px', outline: 'none' }}
                  placeholder="Admin username"
                />
              </div>
              <div>
                <label htmlFor="password" style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#4a5568' }}>Password</label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  style={{ width: '100%', padding: '8px 12px', marginTop: '4px', border: '1px solid #e2e8f0', borderRadius: '4px', outline: 'none' }}
                  placeholder="••••••••"
                />
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <button
                type="button"
                onClick={() => setShowAdminLogin(false)}
                style={{ fontSize: '0.875rem', color: 'rgb(57,46,192)', background: 'none', border: 'none' }}
              >
                Back to Chat
              </button>
              <Button
                className="bg-[rgb(67,56,202)] hover:bg-[rgb(57,46,192)] text-white"
                type="submit"
              >
                Sign in
              </Button>
            </div>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', height: '100vh', backgroundColor: '#f7fafc' }}>
      {/* Global style for bot message links */}
      <style>
        {`
          .bot-message a {
            color: blue;
            text-decoration: underline;
          }
        `}
      </style>

      {/* Left Sidebar */}
      <div style={{ width: '16rem', backgroundColor: 'white', borderRight: '1px solid #edf2f7', display: 'flex', flexDirection: 'column' }}>
        <div style={{ flexGrow: 1, overflowY: 'auto' }}>
          <div style={{ padding: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '16px' }}>
              <div className="flex items-center gap-2">
                <Link
                  to="/"
                  style={{ display: 'flex', alignItems: 'center', gap: '8px', textDecoration: 'none' }}
                >
                  <MessageSquare className="h-6 w-6 text-[rgb(67,56,202)]" />
                  <span className="font-bold text-xl">Genbot</span>
                </Link>
              </div>
            </div>

            {/* Separator */}
            <div style={{ borderBottom: '1px solid #edf2f7', marginBottom: '16px' }} />

            {availableDatabases.length === 0 ? (
              <div>Loading companies...</div>
            ) : (
              <CompanyCards
                universities={displayDatabases}
                selectedUniversity={selectedDatabase ? cleanDatabaseName(selectedDatabase) : null}
                onSelect={handleDatabaseSelect}
                onAdminLogin={() => setShowAdminLogin(true)}
                adminControls={isAdmin}
                initialSettings={chatbotSettings}
                onSaveSettings={handleSaveSettings}
              />
            )}
          </div>
        </div>
        <div style={{ padding: '18.4px', borderTop: '1px solid #edf2f7', flexShrink: 0 }}>
          <Button
            className="bg-[rgb(67,56,202)] hover:bg-[rgb(57,46,192)] text-white"
            onClick={() => {
              if (isAdmin) {
                setIsAdmin(false);
              } else {
                setShowAdminLogin(true);
              }
            }}
            onMouseEnter={() => setLoginHover(true)}
            onMouseLeave={() => setLoginHover(false)}
            style={{ width: '100%', padding: '8px 16px' }}
          >
            {isAdmin ? "Logout" : "Admin Login"}
          </Button>
        </div>
      </div>

      {/* Right Chat Area */}
      {selectedDatabase ? (
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', backgroundColor: 'white', borderBottom: '1px solid #edf2f7', padding: '16px' }}>
            <div style={{ fontSize: '1.25rem', fontWeight: '600', color: '#4338CA' }}>
              {`${cleanDatabaseName(selectedDatabase)} GenBot`}
            </div>
          </div>

          <div style={{ flex: 1, padding: '16px', overflowY: 'auto', backgroundColor: '#f9fafb' }}>
            {chatMessages[selectedDatabase] && chatMessages[selectedDatabase].length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {chatMessages[selectedDatabase].map((msg, index) => {
                  const bubbleStyle = msg.sender === 'user'
                    ? { maxWidth: '350px', borderRadius: '8px', padding: '8px 16px', backgroundColor: '#5a67d8', color: 'white' }
                    : { maxWidth: '600px', borderRadius: '8px', padding: '8px 16px', backgroundColor: 'white', border: '1px solid #edf2f7' };
                  return (
                    <div key={index} style={{ display: 'flex', justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start' }}>
                      <div className={msg.sender === 'bot' ? 'bot-message' : ''} style={bubbleStyle}>
                        {msg.text}
                      </div>
                    </div>
                  );
                })}
                {isBotTyping && (
                  <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
                    <div style={{ maxWidth: '600px', borderRadius: '8px', padding: '8px 16px', backgroundColor: 'white', border: '1px solid #edf2f7', fontStyle: 'italic', color: '#718096' }}>
                      Chatbot is typing...
                    </div>
                  </div>
                )}
                {/* Dummy element to scroll into view */}
                <div ref={messagesEndRef} />
              </div>
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                <div style={{ textAlign: 'center', color: '#718096', padding: '0 16px' }}>
                  <p style={{ fontSize: '1.25rem', marginBottom: '8px' }}>
                    Welcome to {cleanDatabaseName(selectedDatabase)} GenBot
                  </p>
                  <p>Type in your question to start a chat</p>
                </div>
                {/* Dummy element to scroll into view even if there are no messages */}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          <div style={{ backgroundColor: 'white', borderTop: '1px solid #edf2f7', padding: '16px' }}>
            <form onSubmit={handleSendMessage} style={{ display: 'flex' }}>
              <input
                type="text"
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
                placeholder="Ask anything..."
                disabled={isBotTyping}
                style={{ flex: 1, borderTopLeftRadius: '8px', borderBottomLeftRadius: '8px', border: '1px solid #e2e8f0', padding: '8px 16px', outline: 'none' }}
              />
              <Button
                type="submit"
                disabled={isBotTyping}
                className="bg-[rgb(67,56,202)] hover:bg-[rgb(57,46,192)] text-white"
                style={{ padding: '8px 16px', borderBottomLeftRadius: '0px', borderTopLeftRadius: '0px', borderTopRightRadius: '8px', borderBottomRightRadius: '8px', border: 'none' }}
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" style={{ height: '20px', width: '20px' }}>
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
                </svg>
              </Button>
            </form>
          </div>
        </div>
      ) : (
        <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f9fafb' }}>
          <p style={{ fontSize: '1.25rem', color: '#718096' }}>Select a company to start chatting</p>
        </div>
      )}
    </div>
  );
};

export default ChatbotPage;
