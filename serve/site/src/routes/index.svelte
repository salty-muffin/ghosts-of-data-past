<script lang="ts">
	// imports
	import { beforeUpdate, afterUpdate, onMount } from 'svelte';

	import { FontAnimator } from '$lib/components/font-animation';
	import { cubicInOut } from 'svelte/easing';

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

	// handle automatic scrolling
	let messagesWrapper: any;
	let autoscroll: boolean;

	// intersection observer
	let observer: IntersectionObserver | undefined;

	// setting up breathing animation parameters & animators
	const duration = 5000;
	const headerAnimation = new FontAnimator({ weight: 500, italic: 0 }, { weight: 600, italic: 10 });
	let headerC = headerAnimation.getStart();
	const bodyAnimation = new FontAnimator({ weight: 250, italic: 0 }, { weight: 300, italic: 8 });
	let bodyC = bodyAnimation.getStart();
	const timestampAnimation = new FontAnimator(
		{ weight: 350, italic: 0 },
		{ weight: 400, italic: 10 }
	);
	let timestampC = timestampAnimation.getStart();
	onMount(() => {
		// breathing animation
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

		// only animate when in view
		observer = new IntersectionObserver((entries, observer) => {
			entries.forEach(function (entry) {
				// pause/play the animation
				if (entry.isIntersecting) entry.target.classList.add('message--breathing');
				else entry.target.classList.remove('message--breathing');
			});
		});

		// autoscroll to the bottom after returning to the page
		messagesWrapper.scrollTo(0, messagesWrapper.scrollHeight);

		// disable scrolling on this page
		document.body.classList.add('chat--noscroll');

		return () => {
			cancelAnimationFrame(animation);
		};
	});

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

<div
	class="chat"
	style="--h-weight: {headerC.weight}; --h-italic: {headerC.italic}; --b-weight: {bodyC.weight}; --b-italic: {bodyC.italic}; --t-weight: {timestampC.weight}; --t-italic: {timestampC.italic};"
>
	<div class="chat__container">
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
				{#if (index > 0 && message.sender !== $messages[index - 1].sender) || index === 0}
					<div class="chat__spacer" />
					<Message {...message} displaySender={true} attributes={chatAttributes} />
				{:else}
					<Message {...message} displaySender={false} attributes={chatAttributes} />
				{/if}
			{/each}
			{#each $writing as writing_state}
				{#if writing_state.state}
					<!-- add spacer, if current writer differs from the previous message's sender -->
					{#if $messages.length > 0 && writing_state.writer !== $messages[$messages.length - 1].sender}
						<div class="chat__spacer" />
					{/if}
					<Writing writer={writing_state.writer} attributes={chatAttributes} />
				{/if}
			{/each}
		</div>
		<Nav class="chat__nav" links={[{ href: '/story', text: 'documentation' }]} />
	</div>
</div>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.chat--noscroll {
		overflow: hidden;
	}

	.chat {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
	}

	.chat__container {
		height: 100%;

		width: min($chat-width, 100vw);
		height: min($chat-height, 100vh);

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

	.chat__nav {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		flex-shrink: 0;
	}

	@media only screen and (min-width: $chat-width) {
		.chat__container {
			// add borders as the screen grows
			border-left: map-get($border-width, 'lg') solid map-get($colors, 'foreground');
			border-right: map-get($border-width, 'lg') solid map-get($colors, 'foreground');
		}
	}

	@media only screen and (min-height: $chat-height) {
		.chat__container {
			// add borders as the screen grows
			border-top: map-get($border-width, 'lg') solid map-get($colors, 'foreground');
			border-bottom: map-get($border-width, 'lg') solid map-get($colors, 'foreground');
		}
	}

	@media only screen and (min-width: $breakpoint) {
		.chat__container {
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
