<script context="module" lang="ts">
	import type { Load } from '@sveltejs/kit';

	export const load: Load = async ({ error, status }) => ({
		props: { message: error?.message, status }
	});
</script>

<script lang="ts">
	export let message: string;
	export let status: number;
</script>

<div class="error__wrapper">
	<div class="error">
		<h1>{status}</h1>
		<p>{message}</p>
	</div>
</div>

<style lang="scss">
	.error__wrapper {
		height: 100vh;

		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
