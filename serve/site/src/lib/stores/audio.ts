import { writable } from 'svelte/store';

type AudioElement = HTMLAudioElement | null;

function createAudio() {
	const { subscribe, set, update } = writable<AudioElement>(null);

	return {
		subscribe,
		instanciate: (file: string) => {
			set(new Audio(file));
		},
		update: (file: string) =>
			update((audio: AudioElement) => {
				if (audio) {
					audio.src = file;
					return audio;
				} else {
					return null;
				}
			}),
		reset: () => set(null)
	};
}

export const audio = createAudio();
