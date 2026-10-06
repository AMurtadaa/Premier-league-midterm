import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

const teams = ['Arsenal', 'Aston Villa', 'Brentford', 'Brighton and Hove Albion', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham', 'Leeds United', 'Leicester City', 'Liverpool', 'Manchester City', 'Manchester United', 'Newcastle United', 'Norwich City', 'Sheffield United', 'Southampton', 'Tottenham Hotspur', 'Watford', 'West Bromwich Albion', 'West Ham United', 'Wolverhampton Wanderers'];

function App() {
  const [home, setHome] = useState('Arsenal');
  const [away, setAway] = useState('Manchester City');
  const [date, setDate] = useState('');
  const [time, setTime] = useState('15:00');
  const [request, setRequest] = useState(null);
  const [error, setError] = useState('');
  function preview(event) {
    event.preventDefault();
    if (home === away) { setError('Select two different teams.'); setRequest(null); return; }
    setError('');
    setRequest({ home_team: home, away_team: away, date, kickoff_time: time });
  }
  function update(setter, value) { setter(value); setRequest(null); setError(''); }
  return <main>
    <header><a href="#" className="brand">PL<span> / </span>RESEARCH</a><span className="badge">MIDTERM PROTOTYPE</span></header>
    <section className="intro"><p className="eyebrow">PREMIER LEAGUE PREDICTION</p><h1>Every match begins<br />with a question.</h1><p className="subhead">An early interface for exploring match outcomes.<br />Select a fixture to preview the planned model request.</p></section>
    <section className="layout">
      <form onSubmit={preview}>
        <div className="section-heading"><span className="number">01</span><h2>Build your fixture</h2></div>
        <div className="teams">
          <label>HOME TEAM<select value={home} onChange={e => update(setHome, e.target.value)}>{teams.map(team => <option key={team}>{team}</option>)}</select></label>
          <span className="versus" aria-hidden="true">VS</span>
          <label>AWAY TEAM<select value={away} onChange={e => update(setAway, e.target.value)}>{teams.map(team => <option key={team}>{team}</option>)}</select></label>
        </div>
        <div className="schedule"><label>MATCH DATE<input required type="date" value={date} onChange={e => update(setDate, e.target.value)} /></label><label>KICKOFF TIME<input required type="time" value={time} onChange={e => update(setTime, e.target.value)} /></label></div>
        {error && <p role="alert" className="error">{error}</p>}
        <button type="submit">Preview request <span aria-hidden="true">→</span></button>
        <p className="hint">No API call is sent. This is a selection prototype, not a live forecast.</p>
      </form>
      <aside><p className="eyebrow">RESEARCH STATUS</p><h2>The model comes first.</h2><p>Current experiments explore team win versus non-win. The final goal is calibrated home-win, draw and away-win probabilities.</p><ul><li><span className="dot done"></span>Historical data and binary baseline</li><li><span className="dot done"></span>Previous-match rolling features</li><li><span className="dot"></span>Three-class evaluation and calibration</li><li><span className="dot"></span>Prediction API integration</li></ul><div className="notice">Dataset coverage is partial. Results must be evaluated before they become predictions.</div></aside>
    </section>
    {request && <section className="preview" aria-live="polite"><div className="section-heading"><span className="number">02</span><h2>Request preview</h2></div><p>Input validated. A future service will receive these fields. No prediction has been generated.</p><pre>{JSON.stringify(request, null, 2)}</pre></section>}
    <footer>Weeks 1–7 scope · Reconstructed snapshot · Research in progress</footer>
  </main>;
}
createRoot(document.getElementById('root')).render(<App />);
