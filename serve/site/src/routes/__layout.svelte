<script context="module">
	/** @type {import('@sveltejs/kit').Load} */
	export const load = async ({ url }) => ({ props: { url } });
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

	socket.on('chat_message', (message) => {
		messages.add(message);

		console.log(message);
	});
</script>

<PageTransition {url} duration={2000}>
	<slot />
</PageTransition>
