<script>
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

<slot />
