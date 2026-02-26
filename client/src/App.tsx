import React from 'react'
import { AuthProvider, useAuth } from './context/AuthContext'
import ChatInterface from './components/ChatInterface'
import Login from './components/Login'
import './index.css'

const AppContent: React.FC = () => {
  const { token } = useAuth();

  return (
    <div className="App" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', background: '#0f172a' }}>
      {token ? <ChatInterface /> : <Login />}
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App
