import React, { useState } from 'react';
import { authApi } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './Login.css';

const Login: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isRegister, setIsRegister] = useState(false);
    const [error, setError] = useState('');
    const { login } = useAuth();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        try {
            if (isRegister) {
                await authApi.register({ full_name: email.split('@')[0], email, password });
                setIsRegister(false);
                setError('Registration successful! Please login.');
            } else {
                const formData = new FormData();
                formData.append('username', email);
                formData.append('password', password);
                const response = await authApi.login(formData);
                login(response.data.access_token);
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || 'An error occurred');
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <h2>{isRegister ? 'Create Account' : 'Welcome Back'}</h2>
                <p>Sign in to TableMind AI Assistant</p>
                <form onSubmit={handleSubmit}>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    {error && <div className="error-msg">{error}</div>}
                    <button type="submit">{isRegister ? 'Register' : 'Login'}</button>
                </form>
                <button className="toggle-btn" onClick={() => setIsRegister(!isRegister)}>
                    {isRegister ? 'Already have an account? Login' : 'Need an account? Register'}
                </button>
            </div>
        </div>
    );
};

export default Login;
