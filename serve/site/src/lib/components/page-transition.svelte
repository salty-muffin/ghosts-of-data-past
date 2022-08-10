<script>
	import { linear } from 'svelte/easing';

	export let url = '';
	export let duration = 500;

	import { blur } from 'svelte/transition';
</script>

{#key url}
	<div
		in:blur={{ duration: duration, delay: duration, easing: linear }}
		out:blur={{ duration: duration, easing: linear }}
		on:introstart={() => {
			// remove scrollbar during tarnsition
			document.body.classList.add('transition--noscroll');
			const messages = document.getElementById('chat__messages');
			messages && messages.classList.add('transition--noscroll');
		}}
		on:outroend={() => {
			// add scrollbar after tarnsition
			document.body.classList.remove('transition--noscroll');
			const messages = document.getElementById('chat__messages');
			messages && messages.classList.remove('transition--noscroll');
		}}
	>
		<slot />
	</div>
{/key}

<style global lang="scss">
	.transition--noscroll {
		overflow-y: hidden;
	}
</style>
