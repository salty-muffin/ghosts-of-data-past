<script lang="ts">
	// imports
	import { beforeUpdate, afterUpdate, onMount } from 'svelte';

	import { messages } from '$lib/stores/messages';

	import Message from '$lib/components/message.svelte';
	import Nav from '$lib/components/nav.svelte';
	import { element } from 'svelte/internal';

	// intersection observer
	let observer: IntersectionObserver | undefined;
	onMount(() => {
		observer = new IntersectionObserver((entries, observer) => {
			entries.forEach(function (entry) {
				// pause/play the animation
				if (entry.isIntersecting) entry.target.classList.add('message--breathing');
				else entry.target.classList.remove('message--breathing');
			});
		});
	});

	// handle automatic scrolling
	let messagesWrapper: any;
	let autoscroll: boolean;

	// keep track of how many elements are already being observed by the IntersectionObserver
	let observedIndex = 0;

	beforeUpdate(() => {
		// check scroll position before update (enable autoscrolling if it as the bottom)
		autoscroll =
			messagesWrapper &&
			messagesWrapper.offsetHeight + messagesWrapper.scrollTop > messagesWrapper.scrollHeight - 20;
	});

	afterUpdate(() => {
		// autoscroll to the bottom after update
		if (autoscroll) messagesWrapper.scrollTo(0, messagesWrapper.scrollHeight);

		// add previously unobserved elements to intersection observer
		$messages.slice(observedIndex).forEach((message) => {
			let element = document.getElementById(message.id);
			if (element) observer?.observe(element);
		});
		observedIndex = $messages.length - 1;
	});
</script>

<svelte:head>
	<title>ghosts of data past</title>
</svelte:head>

<div class="chat">
	<div class="chat__messages" id="chat__messages" bind:this={messagesWrapper}>
		<div class="chat__placeholder" />
		<Message
			id="Zp7nVKxeiaY3UE5B9Ptjnm"
			sender="scientist"
			text="First, I find your quite negative assessment of cybernetics rather sympathetic. The temptation to use principles of cybernetics as a way to tighten the grip on society is indeed a grim risk we face."
			imageURL=""
			alt=""
			timestamp={1651313396942}
		/>
		<Message
			id="aSwWASETCcg3QaukkAFesN"
			sender="artist"
			text=""
			imageURL="seed0000.jpg"
			alt="seed0000"
			timestamp={1651313416949}
		/>
		{#each $messages as message (message.id)}
			<Message {...message} />
		{/each}
	</div>
	<Nav class="nav" />
</div>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.chat {
		height: 100vh;

		max-width: $chat-width;
		margin: auto;

		display: flex;
		flex-direction: column;
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

	@media only screen and (min-width: $chat-width) {
		.chat {
			// add borders as the screen grows
			border-left: map-get($border-width, 'lg') solid map-get($colors, 'foreground');
			border-right: map-get($border-width, 'lg') solid map-get($colors, 'foreground');
		}
	}
</style>
