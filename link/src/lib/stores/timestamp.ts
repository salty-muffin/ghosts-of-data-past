import { writable } from 'svelte/store';

// types
interface Timestamp {
	time: number;
	recording: boolean;
}

function createTimestamp() {
	const { subscribe, set, update } = writable<Timestamp>({ time: 0, recording: false });

	return {
		subscribe,
		start: () => {
			update((timestamp: Timestamp) => {
				return { time: timestamp.time, recording: true };
			});
		},
		stop: () => {
			update((timestamp: Timestamp) => {
				return { time: timestamp.time, recording: false };
			});
		},
		setTime: (time: number) => {
			update((timestamp: Timestamp) => {
				return { time: time, recording: timestamp.recording };
			});
		},
		set,
		update,
		reset: () => set({ time: 0, recording: false })
	};
}

export const timestamp = createTimestamp();
