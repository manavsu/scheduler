import { writable } from 'svelte/store';
import Weekday from '../routes/weekday';
import type PowerSchedule from '../routes/schedule';

export const available_days = writable<Weekday[]>([]);
export let chart_schedule = writable<PowerSchedule|null>();
