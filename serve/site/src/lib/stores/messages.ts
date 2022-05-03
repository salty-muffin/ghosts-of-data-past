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
		reset: () => set([])
	};
}

export const messages = createMessages();
