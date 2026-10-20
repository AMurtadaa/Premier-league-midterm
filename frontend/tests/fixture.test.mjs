import test from 'node:test';
import assert from 'node:assert/strict';
import { DAYS, validateFixture, makeFixtureRequest } from '../src/fixture.mjs';

test('requires both teams', () => assert.match(validateFixture('', 'Chelsea', '14:00', 'Monday'), /both teams/));
test('rejects identical teams', () => assert.match(validateFixture('Arsenal', 'Arsenal', '14:00', 'Monday'), /different teams/));
test('accepts each supported weekday', () => DAYS.forEach(day => assert.equal(validateFixture('Arsenal', 'Chelsea', '14:00', day), '')));
test('rejects invalid times', () => ['25:00', '14:75', 'abc', '14', ''].forEach(time => assert.match(validateFixture('Arsenal', 'Chelsea', time, 'Monday'), /valid kickoff/)));
test('rejects missing and unknown weekdays', () => ['', 'Yesterday'].forEach(day => assert.match(validateFixture('Arsenal', 'Chelsea', '14:00', day), /valid match day/)));
test('produces input-only request without invented probabilities', () => assert.deepEqual(makeFixtureRequest('Arsenal', 'Chelsea', '14:00', 'Monday'), { home_team: 'Arsenal', away_team: 'Chelsea', kickoff_time: '14:00', match_day: 'Monday' }));
test('refuses invalid request construction', () => assert.throws(() => makeFixtureRequest('Arsenal', 'Arsenal', '14:00', 'Monday')));
