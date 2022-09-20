<script lang="ts">
	// props
	let className = '';
	export { className as class };

	// imports
	import { muted } from '$lib/stores/muted';
</script>

<button class="mute-button {className}" on:click>
	{#if $muted}
		<slot name="muted" />
	{:else}
		<slot name="unmuted" />
	{/if}
</button>

<style global lang="scss">
	.mute-button {
		background: none;
		border: none;
		padding: 0;
		cursor: pointer;
	}
</style>
