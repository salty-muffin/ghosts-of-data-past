<script lang="ts">
	import { linear } from 'svelte/easing';
	import { blur } from 'svelte/transition';

	import { beforeNavigate, goto } from '$app/navigation';

	export let duration = 500;

	let onOutroEnd: () => void;

	// set to false since we have just initialized the layout
	let transitioningOut = false;

	// called when page navigation is triggered
	beforeNavigate(async (navigation) => {
		// this should be false on an initial page load
		// or if we succeed navigating after the transition has finished
		if (!transitioningOut) {
			transitioningOut = true;

			// stop the page from routing, so we can wait for the transition
			// but only if navigating on the same page
			if (
				navigation.from &&
				navigation.to &&
				navigation.from.url.origin === navigation.to.url.origin
			)
				navigation.cancel();

			// assign this fresh function to the wrapping div's on:outroend listener
			onOutroEnd = async () => {
				// wait until page navigation has completed
				if (navigation.to) await goto(navigation.to.url);

				// set to false and the div should be rendered with the transition intro
				transitioningOut = false;
			};
		}
	});
</script>

{#if !transitioningOut}
	<div
		in:blur={{ duration: duration, easing: linear }}
		out:blur={{ duration: duration, easing: linear }}
		on:outroend={onOutroEnd}
	>
		<slot />
	</div>
{/if}
