<script context="module" lang="ts">
	import type { Load } from '@sveltejs/kit';
	// /** @type {import('./__types/__layout').Load} */
	export const load: Load = async ({ url }) => ({ props: { url } });
</script>

<script lang="ts">
	// props
	export let url: string;

	// imports
	import '$lib/scss/fonts.scss';
	import '$lib/scss/global.scss';

	import { onMount } from 'svelte';
	import { cubicInOut } from 'svelte/easing';

	import { io } from 'socket.io-client';

	import { FontAnimator } from '$lib/components/font-animation';
	import { messages } from '$lib/stores/messages';
	import { writing } from '$lib/stores/writing';
	import PageTransition from '$lib/components/page-transition.svelte';

	// breathing animation
	// setting up starting parameters & animators
	const duration = 5000;
	const headerAnimation = new FontAnimator({ weight: 500, italic: 0 }, { weight: 600, italic: 10 });
	let headerC = headerAnimation.getStart();
	const bodyAnimation = new FontAnimator({ weight: 325, italic: 0 }, { weight: 375, italic: 6 });
	let bodyC = bodyAnimation.getStart();
	const timestampAnimation = new FontAnimator(
		{ weight: 300, italic: 0 },
		{ weight: 350, italic: 10 }
	);
	let timestampC = timestampAnimation.getStart();
	onMount(() => {
		let animation = requestAnimationFrame(function update(timestamp: number) {
			// calculation ratio
			const pos = Math.abs(((timestamp % (duration * 2)) - duration) / duration);
			const interpolated = cubicInOut(pos);

			// updating all font animations
			headerC = headerAnimation.update(interpolated);
			bodyC = bodyAnimation.update(interpolated);
			timestampC = timestampAnimation.update(interpolated);

			// append next animation frame
			animation = requestAnimationFrame(update);
		});
		return () => {
			cancelAnimationFrame(animation);
		};
	});

	// socket communication
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
		writing.add({ writer: message.sender, state: false });
	});

	// on incoming writing event
	socket.on('writing_state', (event) => {
		writing.add({ writer: event.writer, state: event.state });
	});
</script>

<PageTransition {url} duration={1500}>
	<div
		style="--h-weight:{headerC.weight}; --h-italic:{headerC.italic}; --b-weight:{bodyC.weight}; --b-italic:{bodyC.italic}; --t-weight:{timestampC.weight}; --t-italic:{timestampC.italic}"
	>
		<slot />
	</div>
</PageTransition>
