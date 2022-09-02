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

	// chat wrapper element
	let chat: HTMLElement | undefined;

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

			// updating css variables
			if (chat) {
				chat.style.setProperty('--h-weight', String(headerC.weight));
				chat.style.setProperty('--h-italic', String(headerC.italic));
				chat.style.setProperty('--b-weight', String(bodyC.weight));
				chat.style.setProperty('--b-italic', String(bodyC.italic));
				chat.style.setProperty('--t-weight', String(timestampC.weight));
				chat.style.setProperty('--t-italic', String(timestampC.italic));
			}

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

<div class="chat" bind:this={chat}>
	<div class="chat__container">
		<div class="chat__messages" id="chat__messages" bind:this={messagesWrapper}>
			<div class="chat__placeholder" />

			<Message
				id="Zp7nVKxeiaY3UE5B9Ptjnm"
				sender="scientist"
				text="First, I find your quite negative assessment of cybernetics rather sympathetic. The temptation to use principles of cybernetics as a way to tighten the grip on society is indeed a grim risk we face."
				imageURL=""
				alt=""
				timestamp={1651313396942}
				attributes={chatAttributes}
			/>
			<Message
				id="aSwWASETCcg3QaukkAFesN"
				sender="artist"
				text=""
				imageURL="seed0000.jpg"
				alt="seed0000"
				timestamp={1651313416949}
				attributes={chatAttributes}
				class="message--spaced"
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
			<Message
				id="Zp7nVKxeiaY3UE5B9Ptjnm"
				sender="scientist"
				text="First, I find your quite negative assessment of cybernetics rather sympathetic. The temptation to use principles of cybernetics as a way to tighten the grip on society is indeed a grim risk we face."
				imageURL=""
				alt=""
				timestamp={1651313396942}
				attributes={chatAttributes}
				class="message--spaced"
			/>
			<Message
				id="aSwWASETCcg3QaukkAFesN"
				sender="artist"
				text=""
				imageURL="seed0000.jpg"
				alt="seed0000"
				timestamp={1651313416949}
				attributes={chatAttributes}
				class="message--spaced"
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
			<Writing writer="scientist" attributes={chatAttributes} class="message--spaced" />

			{#each $messages as message, index (message.id)}
				<!-- add top margin, if this message's sender differs from the previous one -->
				<Message
					{...message}
					displaySender={false}
					attributes={chatAttributes}
					class={index > 0 && message.sender !== $messages[index - 1].sender
						? 'message--spaced'
						: ''}
				/>
			{/each}
			{#each $writing as writing_state}
				{#if writing_state.state}
					<!-- add top margin, if current writer differs from the previous message's sender -->
					<Writing
						writer={writing_state.writer}
						attributes={chatAttributes}
						class={$messages.length > 0 &&
						writing_state.writer !== $messages[$messages.length - 1].sender
							? 'message--spaced'
							: ''}
					/>
				{/if}
			{/each}
		</div>
		<Nav class="chat__nav" links={[{ href: '/process', text: 'process' }]} />
	</div>
</div>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.chat--noscroll {
		overflow: hidden;
	}

	html {
		height: -webkit-fill-available;
	}

	.chat {
		position: relative;
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
		max-height: -webkit-fill-available;
	}

	.chat__container {
		width: min($chat-width, 100%);
		height: min($chat-height, 100%);

		display: flex;
		flex-direction: column;

		filter: drop-shadow(0 0 map-get($border-blur, 'sm') map-get($colors, 'foreground'));
	}

	.chat__messages {
		display: flex;
		flex-direction: column;
		flex-grow: 1;

		/* margin-bottom: map-get($nav-size, 'sm'); */

		overflow-y: auto;

		width: 100%;
	}

	.chat__placeholder {
		flex-grow: 1;
		min-height: map-get($margin-secondary, 'sm');
	}

	.message--spaced {
		margin-top: map-get($margin-secondary, 'sm');
	}

	.chat__nav {
		/* position: fixed;
		bottom: 0;
		left: 0;
		right: 0; */
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

		.chat__placeholder {
			min-height: map-get($margin-secondary, 'lg');
		}

		.message--spaced {
			margin-top: map-get($margin-secondary, 'lg');
		}
	}
</style>
