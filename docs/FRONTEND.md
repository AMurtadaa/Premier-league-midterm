# Frontend implementation

The local interface reuses `frontend/src/app/page.tsx`, `ResultPage.tsx`, and the club crests from [AMurtadaa/Premier-league](https://github.com/AMurtadaa/Premier-league), source commit `f8b34f2cdd7f57340d5dd62191a1738fc1fe792d`. The source repository is unchanged. Original logo paths are retained; assets are supplied locally rather than fetched at runtime.

## Available flow

- Purple header, club logos, separate home/away selectors, kickoff time, and historical fixture date.
- Opponent filtering prevents selecting the same club twice.
- Required controls and time-format validation.
- Results screen with both clubs, home-win/draw/away-win estimates, fixture details, and Change fixture navigation that retains inputs.
- JSON request to Flask through the Vite proxy, with error handling and no fallback to sample percentages.

The original source used a random percentage, and an earlier restoration displayed fixed samples. The current interface displays only model estimates returned by Flask. Run `python -m src.recent` and restart Flask to enable a refreshable results feed. The page displays the date of the last recorded result; estimates are uncalibrated and the app does not verify scheduled fixtures.

## Local adaptations

The React/TypeScript components run under Vite, with Tailwind styles and accessible crest labels. Start Flask first from the repository root with `python -m src.api` after installing `requirements.txt`. Then run the frontend in a second terminal:

```powershell
cd frontend
node .\node_modules\vite\bin\vite.js --host 127.0.0.1 --port 5173 --strictPort
```

Open http://127.0.0.1:5173/ and leave the terminal running.

```sh
npm test
npm run build
```

This is a new working integration, not a recovery of the archived Flask service or evidence of an earlier completion date.
