<script lang="ts">
	import { beforeUpdate, afterUpdate } from 'svelte';

	import { messages } from '$lib/stores/messages';

	import Message from '$lib/components/message.svelte';
	import Nav from '$lib/components/nav.svelte';
	import MessageDummy from '$lib/components/message-dummy.svelte';

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
</script>

<svelte:head>
	<title>ghosts of data past</title>
</svelte:head>

<div class="chat">
	<div class="chat__messages" bind:this={messagesWrapper}>
		<div class="chat__placeholder" />
		<MessageDummy
			id="Zp7nVKxeiaY3UE5B9Ptjnm"
			sender="scientist"
			text="First, I find your quite negative assessment of cybernetics rather sympathetic. The temptation to use principles of cybernetics as a way to tighten the grip on society is indeed a grim risk we face."
			imageURL=""
			alt=""
			timestamp={1651313396942}
		/>
		<MessageDummy
			id="aSwWASETCcg3QaukkAFesN"
			sender="artist"
			text=""
			imageURL="seed0000.jpg"
			alt="seed0000"
			timestamp={1651313416949}
		/>
		<!-- {#each $messages as message (message.id)}
			<Message {...message} />
		{/each} -->
	</div>
	<Nav class="nav" />
</div>

<style global lang="scss">
	.chat {
		display: flex;
		flex-direction: column;
		height: 100vh;
	}

	.chat__messages {
		display: flex;
		flex-direction: column;
		flex-grow: 1;

		overflow-y: auto;

		width: 100%;
	}

	.chat__placeholder {
		flex-grow: 1;
	}

	.nav {
		flex-shrink: 0;
	}
</style>
