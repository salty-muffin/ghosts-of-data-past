<script lang="ts">
	import IframePanel from '$lib/components/iframe-panel.svelte';
	import Nav from '$lib/components/nav.svelte';
</script>

<div class="video">
	<IframePanel class="video__panel" url="https://player.vimeo.com/video/636103889" />
	<Nav class="video__nav" links={[{ href: '/abstract', text: 'abstract' }]} />
</div>
<div class="video__text">
	<p>
		This is a video documentation of <em>ghosts of data past</em>.
	</p>
	<p>
		The abstract and all other pages are visbile exactly like this in the artwork. Only this page
		would usually hold the live generated chat of which a short excerpt is here documented.
	</p>
</div>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.video {
		position: relative;
		width: 100vw;
		height: 100vh;
		max-height: -webkit-fill-available;
	}

	.video__panel {
		width: 100%;
		height: 100%;

		z-index: -1;
	}

	.video__nav {
		position: absolute;
		left: 0;
		bottom: 0;
		right: 0;
	}

	.video__text {
		margin: map-get($margin-primary, 'sm');
	}

	@media only screen and (min-width: $breakpoint) {
		.video__text {
			margin: map-get($margin-primary, 'lg');
		}
	}

	@media only screen and (min-width: 80em) {
		.video__elements {
			position: absolute;
			bottom: 0;
			left: 0;
			right: 0;
		}

		.video__text {
			position: absolute;
			bottom: map-get($nav-size, 'lg');
			left: 0;

			margin: 2em;
			padding: 2em;

			width: 22em;

			background-color: map-get($colors, 'background');

			& > *:first-of-type {
				margin-top: 0;
			}
			& > *:last-of-type {
				margin-bottom: 0;
			}
		}
	}
</style>
