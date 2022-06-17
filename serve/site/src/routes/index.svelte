<script lang="ts">
	// imports
	import { beforeUpdate, afterUpdate, onMount } from 'svelte';

	import { messages } from '$lib/stores/messages';
	import { writing } from '$lib/stores/writing';

	import Message from '$lib/components/message.svelte';
	import Writing from '$lib/components/writing.svelte';
	import Nav from '$lib/components/nav.svelte';

	// types
	interface Attributes {
		[key: string]: Attribute;
	}
	interface Attribute {
		position: string;
	}
	interface Settings {
		maxMessages: number;
	}

	// get chat attributes from endpoint
	export let chatAttributes: Attributes;
	export let settings: Settings;

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

	// keep track of how many elements are already being observed by the intersection observer
	let observedIndex = 0;

	// remove messages, if there are more than the limit
	$: if ($messages.length > settings.maxMessages) {
		// unobserve message
		const element = document.getElementById($messages[0].id);
		if (element) observer?.unobserve(element);
		// remove message
		messages.shift();
		// update observed index
		observedIndex -= 1;
	}

	beforeUpdate(() => {
		// check scroll position before update (enable autoscrolling, if is at the bottom)
		autoscroll =
			messagesWrapper &&
			messagesWrapper.offsetHeight + messagesWrapper.scrollTop > messagesWrapper.scrollHeight - 20;
	});

	afterUpdate(() => {
		// autoscroll to the bottom after update
		if (autoscroll) messagesWrapper.scrollTo(0, messagesWrapper.scrollHeight);

		// add previously unobserved elements to intersection observer
		$messages.slice(observedIndex).forEach((message) => {
			const element = document.getElementById(message.id);
			if (element) observer?.observe(element);
		});
		observedIndex = $messages.length - 1;
	});
</script>

<svelte:head>
	<title>ghosts of data past</title>
</svelte:head>

<div class="chat__center">
	<div class="chat">
		<div class="chat__messages" id="chat__messages" bind:this={messagesWrapper}>
			<div class="chat__placeholder" />
			<div class="chat__spacer" />

			<Message
				id="Zp7nVKxeiaY3UE5B9Ptjnm"
				sender="scientist"
				text="First, I find your quite negative assessment of cybernetics rather sympathetic. The temptation to use principles of cybernetics as a way to tighten the grip on society is indeed a grim risk we face."
				imageURL=""
				alt=""
				timestamp={1651313396942}
				attributes={chatAttributes}
			/>
			<div class="chat__spacer" />
			<Message
				id="aSwWASETCcg3QaukkAFesN"
				sender="artist"
				text=""
				imageURL="seed0000.jpg"
				alt="seed0000"
				timestamp={1651313416949}
				attributes={chatAttributes}
			/>
			<Message
				id="qDwLOSAKCcg3Qaukkpaesd"
				sender="artist"
				text="Here I am."
				imageURL=""
				alt=""
				timestamp={1651313416949}
				displaySender={false}
				attributes={chatAttributes}
			/>
			<Writing writer="scientist" attributes={chatAttributes} />

			{#each $messages as message, index (message.id)}
				<!-- add spacer, if this message's sender differs from the previous one -->
				{#if index > 0 && message.sender !== $messages[index - 1].sender}
					<div class="chat__spacer" />
					<Message {...message} displaySender={true} attributes={chatAttributes} />
				{:else}
					<Message {...message} displaySender={false} attributes={chatAttributes} />
				{/if}
			{/each}
			{#each $writing as writing_state}
				{#if writing_state.state}
					<!-- add spacer, if current writer differs from the previous message's sender -->
					{#if writing_state.writer !== $messages[$messages.length - 1].sender}
						<div class="chat__spacer" />
					{/if}
					<Writing writer={writing_state.writer} attributes={chatAttributes} />
				{/if}
			{/each}
		</div>
		<Nav class="nav" />
	</div>
</div>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.chat__center {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
	}

	.chat {
		height: 100%;

		max-width: $chat-width;
		max-height: $chat-height;
		/* margin: auto; */

		display: flex;
		flex-direction: column;

		filter: drop-shadow(0 0 map-get($border-blur, 'sm') map-get($colors, 'foreground'));
	}

	.chat__messages {
		display: flex;
		flex-direction: column;
		flex-grow: 1;

		margin-bottom: map-get($nav-size, 'sm');

		overflow-y: auto;

		width: 100%;
	}

	.chat__placeholder {
		flex-grow: 1;
	}

	.chat__spacer {
		height: map-get($margin-secondary, 'sm');
		flex-shrink: 0;
	}

	.nav {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		flex-shrink: 0;
	}

	@media only screen and (min-width: $chat-width) {
		.chat {
			// add borders as the screen grows
			border-left: map-get($border-width, 'lg') solid map-get($colors, 'foreground');
			border-right: map-get($border-width, 'lg') solid map-get($colors, 'foreground');
		}
	}

	@media only screen and (min-height: $chat-height) {
		.chat {
			// add borders as the screen grows
			border-top: map-get($border-width, 'lg') solid map-get($colors, 'foreground');
			border-bottom: map-get($border-width, 'lg') solid map-get($colors, 'foreground');
		}
	}

	@media only screen and (min-width: $breakpoint) {
		.chat {
			filter: drop-shadow(0 0 map-get($border-blur, 'lg') map-get($colors, 'foreground'));
		}

		.chat__messages {
			margin-bottom: map-get($nav-size, 'lg');
		}

		.chat__spacer {
			height: map-get($margin-secondary, 'lg');
		}
	}
</style>
