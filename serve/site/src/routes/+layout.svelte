<script lang="ts">
	// imports
	import '$lib/scss/fonts.scss';
	import '$lib/scss/global.scss';

	import { afterNavigate } from '$app/navigation';

	import { io } from 'socket.io-client';

	import { messages } from '$lib/stores/messages';
	import { writing } from '$lib/stores/writing';
	import { muted } from '$lib/stores/muted';
	import { sound } from '$lib/stores/audio';
	import { lost, gate } from '$lib/stores/lost';

	import PageTransition from '$lib/components/page-transition.svelte';

	// socket communication
	const socket = io();

	// on incoming chat message from server
	socket.on('chat_message', (message) => {
		if (!$gate) {
			gate.set(message.gate);
		}
		if ($gate && message.gate !== $gate) {
			lost.set(true);
			socket.disconnect();
		}

		// process image data and if there, create a blob from it
		let imageURL = '';
		if (message.imageData.byteLength > 0) {
			const arrayBufferView = new Uint8Array(message.imageData);
			const blob = new Blob([arrayBufferView], { type: 'image/jpeg' });

			imageURL = URL.createObjectURL(blob);
		}
		// add new message to messages store
		if (!$lost) {
			messages.add({
				id: message.id,
				sender: message.sender,
				text: message.text,
				imageURL: imageURL,
				alt: message.alt,
				timestamp: message.timestamp
			});
		}
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
	});

	// on incoming writing event
	socket.on('writing_state', (event) => {
		if (!$gate) {
			gate.set(event.gate);
		}
		if ($gate && event.gate !== $gate) {
			lost.set(true);
			socket.disconnect();
		}

		if (!$lost) {
			writing.add({ writer: event.writer, state: event.state });
		}
	});

	afterNavigate((navigation) => {
		// disable scrolling on chat
		if (navigation.to?.url.pathname === '/') {
			document.body.classList.add('chat--noscroll');
		} else {
			document.body.classList.remove('chat--noscroll');
		}
	});

	// get random favicon
	const getFavicon = (count: number) => {
		let number = String(Math.floor(Math.random() * count));
		if (number.length < 2) number = `0${number}`;

		return `favicon${number}.png`;
	};
</script>

<!-- show different favicon every time -->
<svelte:head>
	<link rel="icon" type="image/png" href="/favicons/{getFavicon(18)}" />
</svelte:head>

<PageTransition duration={1500}>
	<slot />
</PageTransition>
