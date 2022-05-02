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

<div class="message__wrapper message--{attributes[sender]['position']}" {id}>
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

	@keyframes breathe-sender {
		from {
			font-variation-settings: 'wght' 400, 'ital' 0;
		}
		to {
			font-variation-settings: 'wght' 600, 'ital' 10;
		}
	}
	@keyframes breathe-text {
		from {
			font-variation-settings: 'wght' 425, 'ital' 0;
		}
		to {
			font-variation-settings: 'wght' 375, 'ital' 3;
		}
	}
	@keyframes breathe-timestamp {
		from {
			font-variation-settings: 'wght' 200, 'ital' 0;
		}
		to {
			font-variation-settings: 'wght' 400, 'ital' 10;
		}
	}

	.message__wrapper {
		max-width: 60%;
		margin: 0.5em;
		padding: 0.5em 1em;

		border: 1px solid map-get($colors, 'foreground');
		border-radius: 1em;
	}
	.message--left {
		align-self: flex-start;
	}
	.message--right {
		align-self: flex-end;
	}

	.message__sender {
		margin: 0 0 0.2em 0;

		font-size: 0.9rem;
		animation: 3s ease-in-out 1s infinite alternate both breathe-sender;
	}

	.message__image {
		max-width: 100%;
		height: auto;
	}

	.message__text {
		margin: 0;

		font-size: 0.9rem;
		/* font-variation-settings: 'wght' 400, 'ital' 0; */
		animation: 5s ease-in-out 1s infinite alternate both breathe-text;
	}

	.message__timestamp {
		float: right;
		margin: 0.5em 0 0 0.5em;

		font-size: 0.6rem;
		animation: 3s ease-in-out 1s infinite alternate both breathe-timestamp;
	}
</style>
