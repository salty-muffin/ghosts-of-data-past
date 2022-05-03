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
	@use '../scss/animations' as *;

	.message__wrapper {
		max-width: 60%;

		border: map-get($border-width, 'sm') solid map-get($colors, 'foreground');
		border-radius: map-get($margin-primary, 'sm');

		margin: map-get($margin-secondary, 'sm');
		padding: map-get($margin-secondary, 'sm') map-get($margin-primary, 'sm');
		@media only screen and (min-width: $breakpoint) {
			border-width: map-get($border-width, 'lg');
			border-radius: map-get($margin-primary, 'lg');

			margin: map-get($margin-secondary, 'lg');
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

		animation: 3s ease-in-out 1s infinite alternate both breathe-sender;

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

		animation: 5s ease-in-out 1s infinite alternate both breathe-text;

		line-height: $message-line-height;
		font-size: map-get($message-text-size, 'sm');
		@media only screen and (min-width: $breakpoint) {
			font-size: map-get($message-text-size, 'lg');
		}
	}

	.message__timestamp {
		float: right;
		margin: 0.5em 0 0 0.5em;

		animation: 3s ease-in-out 1s infinite alternate both breathe-timestamp;

		font-size: map-get($timestamp-size, 'sm');
		@media only screen and (min-width: $breakpoint) {
			font-size: map-get($timestamp-size, 'lg');
		}
	}
</style>
