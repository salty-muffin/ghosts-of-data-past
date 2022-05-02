<script>
	export let url = '';
	export let duration = 500;

	import { blur } from 'svelte/transition';
</script>

{#key url}
	<div in:blur={{ duration: duration, delay: duration }} out:blur={{ duration: duration }}>
		<slot />
	</div>
{/key}
