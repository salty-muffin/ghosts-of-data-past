<script context="module" lang="ts">
	export interface Link {
		href: string;
		text: string;
	}
</script>

<script lang="ts">
	// props
	let className = '';
	export { className as class };
	export let links: Link[];

	// imports
	import MuteButton from '$lib/components/mute-button.svelte';
</script>

<div class="nav__wrapper {className}">
	<nav class="nav__links">
		<MuteButton>
			<h4 slot="muted">unmute</h4>
			<h4 slot="unmuted">mute</h4>
		</MuteButton>
		{#each links as link, index (index)}
			<h4><a href={link.href}>{link.text}</a></h4>
		{/each}
	</nav>
</div>

<style global lang="scss">
	@use '../scss/variables' as *;

	.nav__wrapper {
		display: flex;
		align-items: center;

		height: map-get($nav-size, 'sm');

		background-color: map-get($colors, 'background');
	}

	.nav__links {
		width: 100%;
		display: flex;
		flex-wrap: wrap;
		flex-direction: row;
		justify-content: space-between;

		margin: 0 map-get($margin-primary, 'sm');

		h4,
		button {
			font-variation-settings: 'wght' 350;
			font-size: map-get($nav-links-size, 'sm');
			margin: 0;
			text-align: left;
		}
		button:hover h4 {
			font-weight: 350;
		}
	}

	@media (hover: none) {
		button h4 {
			font-weight: 350;
		}
	}

	@media only screen and (min-width: $breakpoint) {
		.nav__wrapper {
			height: map-get($nav-size, 'lg');

			/* border-width: map-get($border-width, 'lg'); */
		}

		.nav__links {
			margin: 0 map-get($margin-primary, 'lg');

			h4 button,
			h4 {
				font-size: map-get($nav-links-size, 'lg');
			}
		}
	}
</style>
