<svelte:options immutable />

<script lang="ts">
	// props
	export let id: string;
	export let sender: string;
	export let text: string;
	export let imageURL: string;
	export let alt: string;
	export let timestamp: number;
	export let attributes: any;
	export let displaySender = true;
	let className = '';
	export { className as class };

	import { fade } from 'svelte/transition';

	// get date from timestamp
	const date = new Date(timestamp);

	// show the image as a banner or not
	let showLargeImage = false;
	const width = 1024;
	const height = 1024;
</script>

<div
	class="message__wrapper message--{attributes[sender]['position']} message--breathing {className}"
	{id}
>
	<div class="message__body">
		{#if displaySender}
			<h6 class="message__sender">{sender}</h6>
		{/if}
		{#if imageURL}
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<img
				class="message__image"
				src={imageURL}
				{alt}
				{width}
				{height}
				on:click={() => {
					showLargeImage = true;
				}}
			/>
		{/if}
		{#if text}
			<span class="message__text">{text}</span>
		{/if}
		<span class="message__timestamp"
			>{date.getHours()}:{date.getMinutes().toString().padStart(2, '0')}</span
		>
	</div>
	<svg
		class="message__tip"
		width="25"
		height="21"
		viewBox="0 0 25 21"
		xmlns="http://www.w3.org/2000/svg"
	>
		<path d="M9 0C9 16 1 20 1 20C1 20 9 16 25 16" />
	</svg>
</div>
{#if imageURL && showLargeImage}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<div
		class="message__image-large"
		transition:fade={{ duration: 1000 }}
		on:click={() => {
			showLargeImage = false;
		}}
	>
		<img class="message__image" src={imageURL} {alt} {width} {height} />
	</div>
{/if}

<style global lang="scss">
	@use '../scss/variables' as *;

	.message__wrapper {
		position: relative;
		max-width: 60%;

		background-color: map-get($colors, 'background');
		border-radius: map-get($margin-primary, 'sm');

		margin-left: map-get($margin-secondary, 'sm');
		margin-right: map-get($margin-secondary, 'sm');
		margin-bottom: map-get($margin-secondary, 'sm');
		padding: map-get($margin-secondary, 'sm') map-get($margin-primary, 'sm');
	}
	.message--left {
		align-self: flex-start;

		.message__tip {
			left: map-get($margin-secondary, 'sm') * (-1);
			margin-left: -0.03em;
		}
	}
	.message--right {
		align-self: flex-end;

		.message__tip {
			right: map-get($margin-secondary, 'sm') * (-1);
			margin-right: -0.03em;

			transform: scaleX(-1);
		}
	}

	.message__sender {
		margin: 0 0 0.2em 0;

		// non-breathing setting
		font-variation-settings: 'wght' 500, 'ital' 0;

		font-size: map-get($sender-size, 'sm');
	}

	.message__image {
		display: block;
		max-width: 100%;
		height: auto;

		cursor: pointer;
	}

	.message__image-large {
		position: absolute;
		inset: 0;

		cursor: pointer;

		background-color: transparentize(map-get($colors, 'background'), 0.2);

		display: flex;
		justify-content: center;
		align-items: center;

		z-index: 1;
	}

	.message__text {
		margin: 0;

		// non-breathing setting
		font-variation-settings: 'wght' 250, 'ital' 0;

		line-height: map-get($message-line-height, 'sm');
		font-size: map-get($message-text-size, 'sm');
	}

	.message__timestamp {
		float: right;
		margin: 0.5em 0 0 0.5em;

		// non-breathing setting
		font-variation-settings: 'wght' 350, 'ital' 0;

		font-size: map-get($timestamp-size, 'sm');
	}

	.message__tip {
		fill: map-get($colors, 'background');
		position: absolute;
		bottom: -0.3em;
		width: map-get($margin-primary, 'sm') + map-get($margin-secondary, 'sm');
		height: auto;
	}

	.message--breathing {
		.message__sender {
			font-variation-settings: 'wght' var(--h-weight), 'ital' var(--h-italic);
		}
		.message__text {
			font-variation-settings: 'wght' var(--b-weight), 'ital' var(--b-italic);
		}
		.message__timestamp {
			font-variation-settings: 'wght' var(--t-weight), 'ital' var(--t-italic);
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'md')) {
		.message__wrapper {
			border-radius: map-get($margin-primary, 'lg');

			margin-left: map-get($margin-secondary, 'lg');
			margin-right: map-get($margin-secondary, 'lg');
			margin-bottom: map-get($margin-secondary, 'lg');
			padding: map-get($margin-secondary, 'lg') map-get($margin-primary, 'lg');
		}
		.message--left {
			.message__tip {
				left: map-get($margin-secondary, 'lg') * (-1);
			}
		}
		.message--right {
			.message__tip {
				right: map-get($margin-secondary, 'lg') * (-1);
			}
		}

		.message__sender {
			font-size: map-get($sender-size, 'lg');
		}

		.message__text {
			font-size: map-get($message-text-size, 'lg');
			line-height: map-get($message-line-height, 'lg');
		}

		.message__timestamp {
			font-size: map-get($timestamp-size, 'lg');
		}

		.message__tip {
			position: absolute;
			bottom: -0.35em;
			width: (map-get($margin-primary, 'lg') + map-get($margin-secondary, 'lg'));
		}
	}
</style>
