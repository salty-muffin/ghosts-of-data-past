<script lang="ts">
	// props
	let className = '';
	export { className as class };

	// imports
	import { muted } from '$lib/stores/muted';
	import { sound } from '$lib/stores/audio';
</script>

<div class="nav__wrapper {className}">
	<nav class="nav__links">
		<h4>
			<button
				class="nav__mute-button"
				on:click={() => {
					$muted = !$muted;

					// if the audio elements havn't been set, instanciate them
					if (!$sound) {
						sound.instanciate(
							'data:audio/mpeg;base64,SUQzBAAAAAABEVRYWFgAAAAtAAADY29tbWVudABCaWdTb3VuZEJhbmsuY29tIC8gTGFTb25vdGhlcXVlLm9yZwBURU5DAAAAHQAAA1N3aXRjaCBQbHVzIMKpIE5DSCBTb2Z0d2FyZQBUSVQyAAAABgAAAzIyMzUAVFNTRQAAAA8AAANMYXZmNTcuODMuMTAwAAAAAAAAAAAAAAD/80DEAAAAA0gAAAAATEFNRTMuMTAwVVVVVVVVVVVVVUxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQsRbAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQMSkAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV'
						);
					}
				}}
			>
				{#if $muted}
					unmute
				{:else}
					mute
				{/if}
			</button>
		</h4>
		<h4><a href="/about">about</a></h4>
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
		justify-content: space-between;

		margin: 0 map-get($margin-primary, 'sm');

		h4 button,
		h4 {
			font-variation-settings: 'wght' 300;
			font-size: map-get($nav-links-size, 'sm');
			margin: 0;
		}
	}

	.nav__mute-button {
		background: none;
		border: none;
		padding: 0;
		cursor: pointer;
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
