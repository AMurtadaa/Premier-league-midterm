import test from 'node:test';
import assert from 'node:assert/strict';
import { DAYS, KICKOFF_TIMES, validateFixture, makeFixtureRequest } from '../src/fixture.mjs';

test('kickoff dropdown offers a full day of valid quarter-hour times', () => {
  assert.equal(new Set(KICKOFF_TIMES).size, 96);
  assert.equal(KICKOFF_TIMES[0], '00:00');
  assert.equal(KICKOFF_TIMES.at(-1), '23:45');
  assert.ok(KICKOFF_TIMES.includes('16:30'));
  assert.ok(KICKOFF_TIMES.every(time => validateFixture('Arsenal', 'Chelsea', time, 'Monday') === ''));
});

test('requires both teams', () => assert.match(validateFixture('', 'Chelsea', '14:00', 'Monday'), /both teams/));
test('rejects identical teams', () => assert.match(validateFixture('Arsenal', 'Arsenal', '14:00', 'Monday'), /different teams/));
test('accepts each supported weekday', () => DAYS.forEach(day => assert.equal(validateFixture('Arsenal', 'Chelsea', '14:00', day), '')));
test('rejects invalid times', () => ['25:00', '14:75', 'abc', '14', ''].forEach(time => assert.match(validateFixture('Arsenal', 'Chelsea', time, 'Monday'), /valid kickoff/)));
test('rejects missing and unknown weekdays', () => ['', 'Yesterday'].forEach(day => assert.match(validateFixture('Arsenal', 'Chelsea', '14:00', day), /valid match day/)));
test('produces input-only request without invented probabilities', () => assert.deepEqual(makeFixtureRequest('Arsenal', 'Chelsea', '14:00', 'Monday'), { home_team: 'Arsenal', away_team: 'Chelsea', kickoff_time: '14:00', match_day: 'Monday' }));
test('refuses invalid request construction', () => assert.throws(() => makeFixtureRequest('Arsenal', 'Arsenal', '14:00', 'Monday')));
