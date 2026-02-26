import React, { useState, useRef, useEffect } from 'react';
import { chatApi } from '../services/api';
import './ChatInterface.css';

interface Message {
    sender: 'user' | 'bot';
    text: string;
}

const ChatInterface: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([
        { sender: 'bot', text: 'Hello! I am TableMind AI. How can I assist you with your restaurant data or ordering today?' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMsg = input.trim();
        setMessages(prev => [...prev, { sender: 'user', text: userMsg }]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await chatApi.sendMessage(userMsg);
            setMessages(prev => [...prev, { sender: 'bot', text: response.data.response }]);
        } catch (error) {
            setMessages(prev => [...prev, { sender: 'bot', text: 'Sorry, I encountered an error. Please try again later.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h3>TableMind AI Assistant</h3>
                <span className="status-indicator"></span>
            </div>
            <div className="chat-messages">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`message-bubble ${msg.sender}`}>
                        {msg.text}
                    </div>
                ))}
                {isLoading && <div className="message-bubble bot loading">Typing...</div>}
                <div ref={scrollRef} />
            </div>
            <div className="chat-input-area">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    placeholder="Ask me something..."
                    disabled={isLoading}
                />
                <button onClick={handleSend} disabled={isLoading}>
                    Send
                </button>
            </div>
        </div>
    );
};

export default ChatInterface;
