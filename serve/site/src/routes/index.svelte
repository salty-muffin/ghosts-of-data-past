<script lang="ts">
	import { beforeUpdate, afterUpdate } from 'svelte';
	import { io } from 'socket.io-client';

	import Message from '$lib/components/message.svelte';
	import Nav from '$lib/components/nav.svelte';
	import MessageDummy from '$lib/components/message-dummy.svelte';

	// types
	interface ChatMessage {
		id: string;
		sender: string;
		text: string;
		imageData: ArrayBuffer;
		alt: string;
		timestamp: number;
	}

	// handle automatic scrolling
	let messagesWrapper: any;
	let autoscroll: boolean;

	beforeUpdate(() => {
		messagesWrapper &&
			console.log(`height: ${messagesWrapper.scrollHeight} pos: ${messagesWrapper.scrollTop}`);
		autoscroll =
			messagesWrapper &&
			messagesWrapper.offsetHeight + messagesWrapper.scrollTop > messagesWrapper.scrollHeight - 20;
	});

	afterUpdate(() => {
		console.log(`height: ${messagesWrapper.scrollHeight} pos: ${messagesWrapper.scrollTop}`);
		if (autoscroll) messagesWrapper.scrollTo(0, messagesWrapper.scrollHeight);
	});

	// initialize websocket
	const socket = io();

	// handle incoming messages
	let messages: ChatMessage[] = [];

	socket.on('chat_message', (item) => {
		messages = [...messages, item];

		console.log(item);
	});
</script>

<svelte:head>
	<title>ghosts of data past</title>
</svelte:head>

<div class="wrapper">
	<div class="messages" bind:this={messagesWrapper}>
		<div class="placeholder" />
		<!-- <MessageDummy
			id="Zp7nVKxeiaY3UE5B9Ptjnm"
			sender="artist"
			text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec in erat sagittis, consectetur nulla eu, volutpat orci. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Vestibulum ante ipsum primis in faucibus orci luctus et ultrices"
			imageURL=""
			alt=""
			timestamp={1651313396.9421964}
		/>
		<MessageDummy
			id="aSwWASETCcg3QaukkAFesN"
			sender="scientist"
			text=""
			imageURL="seed0000.jpg"
			alt="seed0000"
			timestamp={1651313416.9493775}
		/> -->
		{#each messages as message}
			<Message {...message} />
		{/each}
	</div>
	<Nav />
</div>

<style lang="scss">
	.wrapper {
		display: flex;
		flex-direction: column;
		height: 100vh;
	}

	.placeholder {
		flex-grow: 1;
	}

	.messages {
		display: flex;
		flex-direction: column;
		flex-grow: 1;

		overflow-y: auto;

		width: 100%;
	}
</style>
