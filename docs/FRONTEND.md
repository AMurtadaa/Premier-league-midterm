# Frontend implementation

The local interface reuses `frontend/src/app/page.tsx`, `ResultPage.tsx`, and the club crests from [AMurtadaa/Premier-league](https://github.com/AMurtadaa/Premier-league), source commit `f8b34f2cdd7f57340d5dd62191a1738fc1fe792d`. The source repository is unchanged. Original logo paths are retained; assets are supplied locally rather than fetched at runtime.

## Available flow

- Purple header, club logos, separate home/away selectors, kickoff time, and weekday.
- Opponent filtering prevents selecting the same club twice.
- Required controls and time-format validation.
- Results screen with both clubs, a two-way display, match details, and Change fixture navigation that retains input values.
- Expandable JSON input preview, with no request sent to a prediction service.

The original source used a random percentage. This adaptation instead displays fixed 60/40 sample values with prominent **not a model prediction** labels. A draw probability is not inferred from the two-way example. Real H/D/A output and model integration remain incomplete.

## Local adaptations

The React/TypeScript components run under the existing Vite setup rather than copying the old Next.js runtime. Tailwind styles are retained. The input controls retain focus while typing; crest images have accessible labels, the sample bar has adjacent side-by-side segments, and the layout stacks on smaller screens. Pure validation/request functions have automated tests.

```powershell
cd frontend
node .\node_modules\vite\bin\vite.js --host 127.0.0.1 --port 5173 --strictPort
```

Open http://127.0.0.1:5173/ and leave the terminal running.

```sh
npm test
npm run build
```

These adaptations are maintenance of the existing frontend, not evidence of an earlier completion date. The report distinguishes the original Weeks 7-8 interface milestone from later API integration.
