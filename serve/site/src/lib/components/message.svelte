<svelte:options immutable />

<script lang="ts">
	// props
	export let id: string;
	export let sender: string;
	export let text: string;
	export let imageURL: string;
	export let alt: string;
	export let timestamp: number;

	// types
	interface Attributes {
		[key: string]: Attribute;
	}
	interface Attribute {
		position: string;
	}

	// import chat attributes
	import data from '$lib/data/chat-attributes.json';
	const attributes: Attributes = data;

	// get date from timestamp
	const date = new Date(timestamp);
</script>

<div class="message__wrapper message--{attributes[sender]['position']} message--breathing" {id}>
	<h6 class="message__sender">{sender}</h6>
	{#if imageURL}
		<img class="message__image" src={imageURL} {alt} width="1024" height="1024" />
	{/if}
	{#if text}
		<span class="message__text">{text}</span>
	{/if}
	<span class="message__timestamp"
		>{date.getHours()}:{date.getMinutes().toString().padStart(2, '0')}</span
	>
</div>

<style global lang="scss">
	@use '../scss/variables' as *;

	.message__wrapper {
		max-width: 60%;

		border: map-get($border-width, 'sm') solid map-get($colors, 'foreground');
		border-radius: map-get($margin-primary, 'sm');

		margin: 0 map-get($margin-secondary, 'sm') map-get($margin-primary, 'sm');
		padding: map-get($margin-secondary, 'sm') map-get($margin-primary, 'sm');
		@media only screen and (min-width: $breakpoint) {
			border-width: map-get($border-width, 'lg');
			border-radius: map-get($margin-primary, 'lg');

			margin: 0 map-get($margin-secondary, 'lg') map-get($margin-primary, 'lg');
			padding: map-get($margin-secondary, 'lg') map-get($margin-primary, 'lg');
		}
	}
	.message--left {
		align-self: flex-start;
	}
	.message--right {
		align-self: flex-end;
	}

	.message__sender {
		margin: 0 0 0.2em 0;

		font-variation-settings: 'wght' 550, 'ital' 0;

		font-size: map-get($sender-size, 'sm');
		@media only screen and (min-width: $breakpoint) {
			font-size: map-get($sender-size, 'lg');
		}
	}

	.message__image {
		max-width: 100%;
		height: auto;
	}

	.message__text {
		margin: 0;

		font-variation-settings: 'wght' 400, 'ital' 0;

		line-height: $message-line-height;
		font-size: map-get($message-text-size, 'sm');
		@media only screen and (min-width: $breakpoint) {
			font-size: map-get($message-text-size, 'lg');
		}
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

	.message__timestamp {
		float: right;
		margin: 0.5em 0 0 0.5em;

		font-variation-settings: 'wght' 325, 'ital' 0;

		font-size: map-get($timestamp-size, 'sm');
		@media only screen and (min-width: $breakpoint) {
			font-size: map-get($timestamp-size, 'lg');
		}
	}
</style>
