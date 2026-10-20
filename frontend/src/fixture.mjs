export const DAYS = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

export function validateFixture(homeTeam, awayTeam, matchTime, matchDay) {
  if (!homeTeam || !awayTeam) return 'Please select both teams.';
  if (homeTeam === awayTeam) return 'Please select different teams for home and away.';
  if (!/^([01]\d|2[0-3]):[0-5]\d$/.test(matchTime)) return 'Enter a valid kickoff time in HH:MM format.';
  if (!DAYS.includes(matchDay)) return 'Please select a valid match day.';
  return '';
}

export function makeFixtureRequest(homeTeam, awayTeam, matchTime, matchDay) {
  const error = validateFixture(homeTeam, awayTeam, matchTime, matchDay);
  if (error) throw new Error(error);
  return { home_team: homeTeam, away_team: awayTeam, kickoff_time: matchTime, match_day: matchDay };
}
