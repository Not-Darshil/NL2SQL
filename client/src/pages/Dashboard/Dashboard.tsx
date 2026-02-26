import React from 'react';

const Dashboard = () => {
    return (
        <div className="animate-fade" style={{ padding: '40px' }}>
            <header style={{ marginBottom: '40px' }}>
                <h1 className="glow-text" style={{ fontSize: '2.5rem', marginBottom: '8px' }}>Project Dashboard</h1>
                <p style={{ color: 'var(--text-muted)' }}>Overview of your NL2SQL system and database connections.</p>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
                <div className="glass-card">
                    <h3 style={{ marginBottom: '16px' }}>Database Status</h3>
                    <p style={{ color: 'var(--text-muted)', marginBottom: '24px' }}>Connected to PostgreSQL (localhost:5432)</p>
                    <button className="btn-primary">View Schemas</button>
                </div>

                <div className="glass-card">
                    <h3 style={{ marginBottom: '16px' }}>AI Engine</h3>
                    <p style={{ color: 'var(--text-muted)', marginBottom: '24px' }}>Natural Language to SQL conversion is active.</p>
                    <button className="btn-primary">Configure Engine</button>
                </div>

                <div className="glass-card">
                    <h3 style={{ marginBottom: '16px' }}>System Logs</h3>
                    <p style={{ color: 'var(--text-muted)', marginBottom: '24px' }}>Everything stable. 3 queries processed today.</p>
                    <button className="btn-primary">Review Logs</button>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
