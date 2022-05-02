import { writable } from 'svelte/store';

// types
interface Writing {
	writer: string | null;
	writing: boolean;
}

export const writing = writable<Writing>({ writer: null, writing: false });
