import { writable } from 'svelte/store';

// types
interface Message {
	id: string;
	sender: string;
	text: string;
	imageURL: string;
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
		shift: () => {
			update((messages: Message[]) => messages.slice(1));
		},
		set: set,
		update: update,
		reset: () => set([])
	};
}

export const messages = createMessages();
