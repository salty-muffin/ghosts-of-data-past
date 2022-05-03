<script context="module" lang="ts">
	import type { Load } from '@sveltejs/kit';
	export const load: Load = async ({ url }) => ({ props: { url } });
</script>

<script lang="ts">
	export let url: string;
	import PageTransition from '$lib/components/page-transition.svelte';

	import '$lib/scss/fonts.scss';
	import '$lib/scss/global.scss';

	// socket communication
	import { io } from 'socket.io-client';
	import { messages } from '$lib/stores/messages';

	const socket = io();

	// on incoming chat message from server
	socket.on('chat_message', (message) => {
		// process image data and if there, create a blob from it
		let imageURL = '';
		if (message.imageData.byteLength > 0) {
			const arrayBufferView = new Uint8Array(message.imageData);
			const blob = new Blob([arrayBufferView], { type: 'image/jpeg' });

			imageURL = URL.createObjectURL(blob);
		}
		// add new message to messages store
		messages.add({
			id: message.id,
			sender: message.sender,
			text: message.text,
			imageURL: imageURL,
			alt: message.alt,
			timestamp: message.timestamp
		});
	});
</script>

<PageTransition {url} duration={1500}>
	<slot />
</PageTransition>
