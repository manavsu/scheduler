import { writable } from 'svelte/store';
import Weekday from '../routes/weekday';

export const available_days = writable<Weekday[]>([]);
