import { writable } from 'svelte/store';

// types
interface Message {
	id: string;
	sender: string;
	text: string;
	imageData: ArrayBuffer;
	alt: string;
	timestamp: number;
}

function createMessages() {
	const { subscribe, set, update } = writable<Message[]>([]);

	return {
		subscribe,
		add: (message: Message) => {
			update((messages: Message[]) => [...messages, message]);
		},
		reset: () => set([])
	};
}

export const messages = createMessages();
