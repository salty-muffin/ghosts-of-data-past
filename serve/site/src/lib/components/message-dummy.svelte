<script lang="ts">
	// props
	export let id: string;
	export let sender: string;
	export let text: string;
	export let imageURL: string;
	export let alt: string;
	export let timestamp: number;

	import Image from '$lib/components/image.svelte';

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

<div class="message-wrapper {attributes[sender]['position']}" {id}>
	<h6 class="sender">{sender}</h6>
	{#if imageURL}
		<Image class="message-image" src={imageURL} {alt} />
	{/if}
	{#if text}
		<span class="text">{text}</span>
	{/if}
	<span class="timestamp">{date.getHours()}:{date.getMinutes()}</span>
</div>

<style lang="scss">
	@use '../scss/variables' as *;

	.sender {
		margin: 0 0 0.5em 0;

		font-size: 0.8rem;
	}

	.message-wrapper {
		max-width: 60%;
		margin: 0.5em;
		padding: 0.5em 1em;

		border: 1px solid map-get($colors, 'foreground');
		border-radius: 1em;
	}

	:global(.message-image) {
		max-width: 100%;
	}

	.text {
		margin: 0;

		font-size: 0.8rem;
	}

	.timestamp {
		float: right;
		margin: 0.5em 0 0 0.5em;

		font-size: 0.6rem;
	}

	.left {
		align-self: flex-start;
	}

	.right {
		align-self: flex-end;
	}
</style>
