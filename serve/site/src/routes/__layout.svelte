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

	import { onMount } from 'svelte';
	import { cubicInOut } from 'svelte/easing';
	import { io } from 'socket.io-client';
	import { messages } from '$lib/stores/messages';

	import PageTransition from '$lib/components/page-transition.svelte';

	// breathing animation
	const duration = 5000;
	const start = { weight: 300, italic: 0 };
	const end = { weight: 500, italic: 5 };
	let current = start;
	onMount(() => {
		let animation = window.requestAnimationFrame(function update(timestamp: number) {
			const pos = Math.abs(((timestamp % (duration * 2)) - duration) / duration);
			const interpolated = cubicInOut(pos);

			current = {
				weight: Math.round((end.weight - start.weight) * interpolated + start.weight),
				italic: Math.round((end.italic - start.italic) * interpolated + start.italic)
			};

			// append next animation frame
			animation = window.requestAnimationFrame(update);
		});
		return () => {
			window.cancelAnimationFrame(animation);
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
	});
</script>

<PageTransition {url} duration={1500}>
	<div style="--weight:{current.weight}; --italic:{current.italic}">
		<slot />
	</div>
</PageTransition>
