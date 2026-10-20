// ResultPage Component

import React, { Dispatch, SetStateAction } from 'react';
import { makeFixtureRequest } from '../fixture.mjs';

interface ResultPageProps {
  setShowResult: Dispatch<SetStateAction<boolean>>;
  homeTeam: string;
  awayTeam: string;
  matchTime: string;
  matchDay: string;
  homeWinPercentage: number; // Add this prop
  homeTeamLogo: string; // Add this prop for home team logo
  awayTeamLogo: string; // Add this prop for away team logo
}

const ResultPage: React.FC<ResultPageProps> = ({
  setShowResult,
  homeTeam,
  awayTeam,
  matchTime,
  matchDay,
  homeWinPercentage,
  homeTeamLogo,
  awayTeamLogo,
}) => {
  // Original two-way display retained for UI demonstration, not inference.
  const awayWinPercentage = 100 - homeWinPercentage;

  const request = makeFixtureRequest(homeTeam, awayTeam, matchTime, matchDay);

  return (
    <div className="flex flex-col items-center min-h-screen w-full bg-gray-100 pb-10">
      <div className='flex items-center w-full bg-purple-950 p-4'>
      <img src="/logo/Priemier league logo image.png" alt="Premier League Logo" className="h-12 w-auto mr-3 object-contain" />
        <h1 className="text-xl font-bold text-white text-center">
          Premier League
        </h1>
        <p className="text-white ml-1"> - Fantasy Predictor</p>
      </div>
      <div className='flex flex-col items-center w-full px-6 max-sm:px-4'>
        <h2 className="text-purple-950 font-bold p-4 text-xl">Results preview</h2>
        <div className="demo-notice" role="status"><strong>Sample display only - not a model prediction.</strong> The 60% / 40% values are fixed layout examples. This original two-way visualization does not represent a home/draw/away probability model.</div>

        {/* Home and Away Teams Wrapper */}
        <div className='result-grid fixture-card'>
          {/* Home Team */}
          <div className='flex flex-col items-center gap-8'>
            <h3 className='font-bold text-purple-950'>{homeTeam}</h3>
            <div className='w-40 h-40'>
              <img src={homeTeamLogo} alt={`${homeTeam} logo`} className='w-full h-full object-contain'/>
            </div>
          </div>

          {/* Percentage Slider */}
          <div className="w-full flex flex-col items-center">
            <p className="text-xs font-bold text-purple-800 mb-4">ILLUSTRATIVE TWO-WAY DISPLAY</p>
            <div className="w-full flex bg-gray-400 rounded-full h-3 overflow-hidden relative" aria-label="Sample values: home 60 percent, away 40 percent">
              <div
                className="bg-red-500 h-full"
                style={{ width: `${homeWinPercentage}%` }}
              ></div>
              <div
                className="bg-blue-500 h-full"
                style={{ width: `${awayWinPercentage}%` }}
              ></div>
            </div>
            <div className="flex justify-between mt-2 w-full">
              <span className="text-purple-950 font-bold">{homeWinPercentage}%</span>
              <span className="text-purple-950 font-bold">{awayWinPercentage}%</span>
            </div>
            <div className="text-center text-purple-950 font-bold mt-2">
              Sample layout - forecast unavailable
            </div>
            <div className="text-center text-purple-950">
              Draw probability and model output will be added after research validation and API integration.
            </div>
          </div>

          {/* Away Team */}
          <div className='flex flex-col items-center gap-8'>
            <h3 className='font-bold text-purple-950'>{awayTeam}</h3>
            <div className='w-40 h-40'>
              <img src={awayTeamLogo} alt={`${awayTeam} logo`} className='w-full h-full object-contain'/>
            </div>
          </div>
        </div>

        <div className="text-purple-950 my-4">
          <h3 className="font-bold">Match Details:</h3>
          <ul className="list-disc ml-6">
            <li>Home Team: {homeTeam}</li>
            <li>Away Team: {awayTeam}</li>
            <li>Match Time: {matchTime}</li>
            <li>Match Day: {matchDay}</li>
          </ul>
        </div>
        <details className="w-full max-w-2xl bg-white border rounded-lg p-4 mb-5">
          <summary className="cursor-pointer font-bold text-purple-950">View request fields</summary>
          <p className="text-sm text-gray-600 mt-3">Prepared input only. No API request has been sent.</p>
          <pre className="text-sm overflow-x-auto p-3 mt-3 bg-gray-100 rounded">{JSON.stringify(request, null, 2)}</pre>
        </details>

        {/* Centered Small Button */}
        <button
          onClick={() => setShowResult(false)}
          className="bg-purple-700 hover:bg-purple-900 text-white font-bold py-3 px-6 rounded text-lg"
        >
          Change fixture
        </button>
      </div>
    </div>
  );
};

export default ResultPage;
