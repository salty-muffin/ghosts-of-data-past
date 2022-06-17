import { writable } from 'svelte/store';

// types
interface Writing {
	writer: string;
	state: boolean;
}

function createWriting() {
	const { subscribe, set, update } = writable<Writing[]>([]);

	return {
		subscribe,
		add: (writing: Writing) => {
			// if (writing.length && writing.some(element => {element.}))
			update((writings: Writing[]) => {
				// remove element with the same writer as incoming, so there are no duplicates
				const temp_writings = writings.filter((element) => element.writer != writing.writer);
				// add incoming writer
				return [...temp_writings, writing];
			});
		},
		set: set,
		update: update,
		reset: () => set([])
	};
}

export const writing = createWriting();
