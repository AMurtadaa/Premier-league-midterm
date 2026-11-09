import React, { useEffect, useState } from 'react';
import ResultPage, { type Prediction } from './ResultPage';
import { KICKOFF_TIMES, validateFixture } from '../fixture.mjs';

interface Team {
  name: string;
  logo: string;
}

interface Coverage {
  min_date: string;
  max_date: string;
  last_result: string;
  source: string;
  active_since?: string;
  active_teams?: string[];
}

const clubName = (name: string) => name === 'Brighton & Hove Albion' ? 'Brighton and Hove Albion' : name;

const teams: Team[] = [
  { name: 'Arsenal', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/arsenal.football-logos.cc.png' },
  { name: 'Aston Villa', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/aston-villa.football-logos.cc.png' },
  { name: 'Bournemouth', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/bournemouth.football-logos.cc.png' },
  { name: 'Brentford', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/brentford.football-logos.cc.png' },
  { name: 'Brighton & Hove Albion', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/brighton.football-logos.cc.png' },
  { name: 'Burnley', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/burnley.football-logos.cc.png' },
  { name: 'Chelsea', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/chelsea.football-logos.cc.png' },
  { name: 'Crystal Palace', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/crystal-palace.football-logos.cc.png' },
  { name: 'Everton', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/everton.football-logos.cc.png' },
  { name: 'Fulham', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/fulham.football-logos.cc.png' },
  { name: 'Leeds United', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/leeds-united.football-logos.cc.png' },
  { name: 'Liverpool', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/liverpool.football-logos.cc.png' },
  { name: 'Manchester City', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/manchester-city.football-logos.cc.png' },
  { name: 'Manchester United', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/manchester-united.football-logos.cc.png' },
  { name: 'Newcastle United', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/newcastle.football-logos.cc.png' },
  { name: 'Nottingham Forest', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/nottingham-forest.football-logos.cc.png' },
  { name: 'Sunderland', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/sunderland.football-logos.cc.png' },
  { name: 'Tottenham Hotspur', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/tottenham.football-logos.cc.png' },
  { name: 'West Ham United', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/west-ham.football-logos.cc.png' },
  { name: 'Wolverhampton Wanderers', logo: '/logo/english-premier-league-2025-2026.football-logos.cc/1500x1500/wolves.football-logos.cc.png' },
];


const Page: React.FC = () => {
  const [homeTeam, setHomeTeam] = useState<Team | null>(teams.find(team => team.name === 'Manchester City')!);
  const [awayTeam, setAwayTeam] = useState<Team | null>(teams.find(team => team.name === 'Manchester United')!);
  const [matchTime, setMatchTime] = useState('16:30');
  const [matchDate, setMatchDate] = useState('2022-03-06');
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');
  const [coverage, setCoverage] = useState<Coverage | null>(null);
  const [coveredClubs, setCoveredClubs] = useState<string[]>([]);
  useEffect(() => {
    const controller = new AbortController();
    fetch('/api/status', { signal: controller.signal })
      .then(response => {
        if (!response.ok) throw new Error('Unable to load match data.');
        return response.json();
      })
      .then(status => {
        setCoverage(status.coverage);
        setCoveredClubs(status.teams);
        if (status.coverage.active_since) {
          const today = new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/London', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date());
          setMatchDate(today <= status.coverage.max_date ? today : status.coverage.last_result);
        }
      })
      .catch(err => { if (err.name !== 'AbortError') setError('Could not load match data. Check that Flask is running.'); });
    return () => controller.abort();
  }, []);
  const eligible = coverage?.active_since && matchDate >= coverage.active_since
    ? coverage.active_teams ?? coveredClubs : coveredClubs;
  const clubOptions = eligible.map(name => teams.find(team => clubName(team.name) === name) ?? { name, logo: '' });
  const changeDate = (day: string) => {
    setMatchDate(day);
    if (coverage?.active_since && day >= coverage.active_since) {
      if (homeTeam && !coverage.active_teams?.includes(clubName(homeTeam.name))) setHomeTeam(null);
      if (awayTeam && !coverage.active_teams?.includes(clubName(awayTeam.name))) setAwayTeam(null);
    }
  };

  const handleHomeTeamChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedTeam = clubOptions.find((team) => team.name === event.target.value);
    setHomeTeam(selectedTeam || null);
  };

  const handleAwayTeamChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedTeam = clubOptions.find((team) => team.name === event.target.value);
    setAwayTeam(selectedTeam || null);
  };

  const handleMatchTimeChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setMatchTime(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (pending) return;
    const matchDay = new Date(matchDate + 'T00:00:00Z').toLocaleDateString('en-US', { weekday: 'long', timeZone: 'UTC' });
    const validationError = validateFixture(homeTeam?.name, awayTeam?.name, matchTime, matchDay);
    if (validationError) {
      setError(validationError);
      return;
    }
    setError('');
    setPending(true);
    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ home_team: homeTeam?.name, away_team: awayTeam?.name, match_date: matchDate, kickoff_time: matchTime }),
        signal: AbortSignal.timeout(30000),
      });
      const result = await response.json().catch(() => null);
      if (!response.ok) throw new Error(result?.error ?? 'The prediction service is unavailable. Check that Flask is running.');
      const values = ['home_win', 'draw', 'away_win'].map(key => result?.probabilities?.[key]);
      if (!values.every(value => typeof value === 'number' && Number.isFinite(value) && value >= 0 && value <= 1)
          || Math.abs(values.reduce((a, b) => a + b, 0) - 1) > 0.0001) {
        throw new Error('The prediction service returned an invalid response.');
      }
      setPrediction(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to reach the prediction service.');
    } finally {
      setPending(false);
    }
  };

  if (prediction) {
    return (
      <ResultPage
        onBack={() => setPrediction(null)}
        homeTeam={homeTeam?.name || ''}
        awayTeam={awayTeam?.name || ''}
        prediction={prediction}
        homeTeamLogo={homeTeam ? homeTeam.logo : ""}
        awayTeamLogo={awayTeam ? awayTeam.logo : ""}
      />
    );
  }

  const TeamSelector = ({ title, value, onChange, selectedTeamName }: { title: string, value: Team | null, onChange: (event: React.ChangeEvent<HTMLSelectElement>) => void, selectedTeamName?: string }) => {
    const availableTeams = selectedTeamName
      ? clubOptions.filter(team => team.name !== selectedTeamName)
      : clubOptions;

    return (
      <div className='flex flex-col items-center gap-8'>
        <h3 className='font-bold text-purple-950'>{title}</h3>
        <div className='w-40 h-40 flex items-center justify-center'>
          {value?.logo ? <img src={value.logo} alt={`${value.name} crest`} className='w-full h-full object-contain'/> : <span className='text-sm text-gray-500'>{value?.name ?? 'Choose a club'}</span>}
        </div>
        <select
          className="w-full border border-gray-400 rounded px-3 py-2  text-black"
          onChange={onChange}
          value={value?.name || ''}
          aria-label={title === 'HOME TEAM' ? 'Home team' : 'Away team'}
          disabled={pending}
          required
        >
          <option value="" className='text-slate-400'>Select a team</option>
          {availableTeams.map((team) => (
            <option key={team.name} value={team.name}>
              {team.name}
            </option>
          ))}
        </select>
      </div>
    )
  }

  const PredictorFormMain = () => {
    return (
      <div className="flex flex-col items-center gap-2">
        <label htmlFor="match-time" className="text-purple-950 font-bold">Match Time</label>
        <div className="flex flex-col gap-4 w-full text-center">
          <select
            id="match-time"
            className="w-full border border-gray-400 rounded bg-white px-3 py-2 text-black"
            onChange={handleMatchTimeChange}
            value={matchTime}
            disabled={pending}
            required
          >
            {KICKOFF_TIMES.map((time) => (
              <option key={time} value={time}>{time}</option>
            ))}
          </select>
          <h3 className="text-purple-950 font-bold">Match Date</h3>
          <input
            type="date"
            className="w-full border border-gray-400 rounded px-3 py-2  text-black"
            onChange={event => changeDate(event.target.value)}
            value={matchDate}
            min={coverage?.min_date}
            max={coverage?.max_date}
            aria-label="Match date"
            disabled={pending}
            required
          />
        </div>
        <button
          type="submit"
          className="bg-purple-700 hover:bg-purple-900 text-white font-bold py-3 px-6 rounded text-lg disabled:bg-purple-400 disabled:hover:cursor-default hover:cursor-pointer"
          disabled={pending || !coverage || !homeTeam || !awayTeam || !matchTime || !matchDate}
        >
          {pending ? 'Predicting…' : 'Predict match'}
        </button>
      </div>
    )
  }

  return (
    <div className="flex flex-col items-center min-h-screen w-full bg-gray-100 pb-8">
      <div className='flex items-center w-full bg-purple-950 p-4'>
      <img src="/logo/Priemier league logo image.png" alt="Premier League Logo" className="h-12 w-auto mr-3 object-contain" />
        <h1 className="text-xl font-bold text-white text-center">
          Premier League
        </h1>
        <p className="text-white ml-1"> - Fantasy Predictor</p>
      </div>
      <div className='flex flex-col items-center w-full'>
        <h2 className="text-purple-950 font-bold p-4 text-xl">Match Predictor</h2>
        <p className="text-sm text-purple-950 mb-3 px-4 text-center">
          {coverage ? `Match results through ${coverage.last_result} · ${coverage.source}` : 'Loading match coverage…'}
        </p>
        <form
          onSubmit={handleSubmit}
          className="fixture-grid fixture-card mx-4">
          {/* Home Team */}
          {TeamSelector({ title: 'HOME TEAM', value: homeTeam, onChange: handleHomeTeamChange, selectedTeamName: awayTeam?.name })}

          {/* Match Time and Day and Submit*/}
          {PredictorFormMain()}

          {/* Away Team */}
          {TeamSelector({ title: 'AWAY TEAM', value: awayTeam, onChange: handleAwayTeamChange, selectedTeamName: homeTeam?.name })}
        </form>
        {error && <p role="alert" className="text-red-700 mt-4">{error}</p>}
      </div>

    </div>
  );
};

export default Page;
