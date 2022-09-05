<script context="module" lang="ts">
	import type { Load } from '@sveltejs/kit';

	export const load: Load = async ({ url }) => ({ props: { url } });
</script>

<script lang="ts">
	// props
	export let url: string;

	// imports
	import '$lib/scss/fonts.scss';
	import '$lib/scss/global.scss';

	import { afterNavigate } from '$app/navigation';

	import { io } from 'socket.io-client';

	import { messages } from '$lib/stores/messages';
	import { writing } from '$lib/stores/writing';
	import { muted } from '$lib/stores/muted';
	import { sound } from '$lib/stores/audio';

	import PageTransition from '$lib/components/page-transition.svelte';

	// socket communication
	const socket = io();

	// on incoming chat message from server
	socket.on('chat_message', (message) => {
		// take care that message is only processed, if sender has been writing before
		if ($writing.filter((element) => element.writer === message.sender).length > 0) {
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
			writing.add({ writer: message.sender, state: false });

			// play audio on new message (only if unmuted)
			if (!$muted && $sound) {
				// create a blob from sound data
				const arrayBufferView = new Uint8Array(message.soundData);
				const blob = new Blob([arrayBufferView], { type: 'audio/mpeg' });

				const soundURL = URL.createObjectURL(blob);

				if ($sound) $sound.src = soundURL;
				$sound.play();
			}
		}
	});

	// on incoming writing event
	socket.on('writing_state', (event) => {
		writing.add({ writer: event.writer, state: event.state });
	});

	const transitionDuration = 1500;
	afterNavigate((navigation) => {
		// disable scrolling on chat
		if (navigation.to.pathname === '/') {
			document.body.classList.add('chat--noscroll');
		} else {
			document.body.classList.remove('chat--noscroll');
		}
	});
</script>

<PageTransition {url} duration={transitionDuration}>
	<slot />
</PageTransition>
