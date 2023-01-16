<script lang="ts">
	import Footer from '$lib/components/footer.svelte';
</script>

<div class="doc">
	<article class="doc__container">
		<main class="other__content">
			<slot />
		</main>
	</article>
	<Footer />
</div>

<style global lang="scss">
	@use '../../lib/scss/variables' as *;

	.other__title {
		font-size: map-get($title-size, 'sm');
		font-family: $font-family-text;
		hyphens: auto;
		letter-spacing: unset;
	}

	.other__content {
		// font-feature-settings: 'ss01' 1;

		p:first-of-type {
			margin-top: 0;
		}

		li > p {
			margin: 0;
		}

		h1,
		h2,
		h3 {
			scroll-margin-top: 0.5em;

			text-align: left;
			margin-top: 1.5em;

			font-family: $font-family-text;
			// font-variation-settings: 'wght' 550, 'ital' 5;
			text-transform: none;
			letter-spacing: unset;
			hyphens: auto;
		}

		.doc__toc {
			display: none;
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'md')) {
		.other__title {
			margin: 1.5em 0;

			font-size: map-get($title-size, 'md');
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'lg')) {
		.other__title {
			margin: 1.5em 0;

			font-size: map-get($title-size, 'lg');
		}
	}
</style>
