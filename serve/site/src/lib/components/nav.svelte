<script lang="ts">
	// props
	let className = '';
	export { className as class };

	// imports
	import { muted } from '$lib/stores/muted';
	import { audio } from '$lib/stores/audio';
</script>

<div class="nav__wrapper {className}">
	<nav class="nav__links">
		<button
			class="nav__mute-button"
			on:click={() => {
				$muted = !$muted;

				// if the audio element hasn't been set, instanciate it
				if (!$audio) {
					audio.instanciate('fused.mp3');
				}
			}}
		>
			<h3>
				{#if $muted}
					unmute
				{:else}
					mute
				{/if}
			</h3>
		</button>
		<h3><a href="/about">about</a></h3>
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

		h3 {
			font-weight: normal;
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
		}
	}
</style>
