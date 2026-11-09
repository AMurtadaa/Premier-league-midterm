import React from 'react';

export interface Prediction {
  probabilities: { home_win: number; draw: number; away_win: number };
  model: string;
  calibrated: boolean;
  match_date: string;
  kickoff_time: string;
  last_result?: string;
}

interface Props {
  prediction: Prediction;
  onBack: () => void;
  homeTeam: string;
  awayTeam: string;
  homeTeamLogo: string;
  awayTeamLogo: string;
}

export default function ResultPage({ prediction, onBack, homeTeam, awayTeam, homeTeamLogo, awayTeamLogo }: Props) {
  const outcomes = [
    { name: 'Home win', value: prediction.probabilities.home_win, color: 'bg-red-600' },
    { name: 'Draw', value: prediction.probabilities.draw, color: 'bg-purple-500' },
    { name: 'Away win', value: prediction.probabilities.away_win, color: 'bg-blue-600' },
  ];
  return (
    <main className="flex flex-col items-center min-h-screen w-full bg-gray-100 pb-10">
      <header className="flex items-center w-full bg-purple-950 p-4">
        <img src="/logo/Priemier league logo image.png" alt="Premier League Logo" className="h-12 w-auto mr-3 object-contain" />
        <h1 className="text-xl font-bold text-white">Premier League - Fantasy Predictor</h1>
      </header>
      <section className="flex flex-col items-center w-full px-6 max-sm:px-4">
        <h2 className="text-purple-950 font-bold p-4 text-xl">Match prediction</h2>
        <div className="result-grid fixture-card">
          <div className="flex flex-col items-center gap-4">
            <h3 className="font-bold">{homeTeam}</h3>
            {homeTeamLogo && <img src={homeTeamLogo} alt={homeTeam + ' crest'} className="w-40 h-40 object-contain" />}
          </div>
          <div className="w-full">
            <div className="w-full flex rounded-full h-3 overflow-hidden" aria-hidden="true">
              {outcomes.map(item => <div key={item.name} className={item.color} style={{width: item.value * 100 + '%'}} />)}
            </div>
            <dl className="grid grid-cols-3 gap-2 mt-4 text-center">
              {outcomes.map(item => <div key={item.name}><dt className="text-sm">{item.name}</dt><dd className="text-lg font-bold">{(item.value * 100).toFixed(1)}%</dd></div>)}
            </dl>
          </div>
          <div className="flex flex-col items-center gap-4">
            <h3 className="font-bold">{awayTeam}</h3>
            {awayTeamLogo && <img src={awayTeamLogo} alt={awayTeam + ' crest'} className="w-40 h-40 object-contain" />}
          </div>
        </div>
        <p className="my-4 text-center">{prediction.match_date} · {prediction.kickoff_time} · {prediction.model}</p>
        <button onClick={onBack} className="bg-purple-700 hover:bg-purple-900 text-white font-bold py-3 px-6 rounded">Change fixture</button>
      </section>
    </main>
  );
}
