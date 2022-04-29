<script lang="ts">
	import { io } from 'socket.io-client';

	import ChatMessage from '../lib/components/chat-message.svelte';
	import ChatImage from '../lib/components/chat-image.svelte';

	interface ChatItem {
		type: string;
		text: string;
		imageData: ArrayBuffer;
	}

	const socket = io();

	let messages: ChatItem[] = [];

	socket.on('chat_item', (item) => {
		messages = [...messages, item];
	});
</script>

<svelte:head>
	<title>ghosts of data past</title>
</svelte:head>

<h1>messages</h1>
{#each messages as message}
	{#if message.type === 'message'}
		<ChatMessage text={message.text} />
	{:else if message.type === 'image'}
		<ChatImage text={message.text} imageData={message.imageData} />
	{/if}
{/each}
