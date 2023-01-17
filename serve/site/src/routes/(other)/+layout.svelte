<script lang="ts">
	import Nav from '$lib/components/nav.svelte';
	import MuteButton from '$lib/components/mute-button.svelte';
	import Footer from '$lib/components/footer.svelte';
</script>

<div class="doc">
	<article class="doc__container">
		<Nav
			class="doc__nav"
			links={[
				{ href: '/', text: 'back to work' },
				{ href: '/background', text: 'background' },
				{ href: '/credits', text: 'credits' },
				{ href: '/source', text: 'source' }
			]}
		>
			<MuteButton>
				<h4 slot="muted">unmute</h4>
				<h4 slot="unmuted">mute</h4>
			</MuteButton>
		</Nav>
		<main class="other__content">
			<slot />
		</main>
	</article>
	<Footer />
</div>

<style global lang="scss">
	@use '../../lib/scss/variables' as *;

	.other__content {
		// font-feature-settings: 'ss01' 1;

		.other__title {
			height: map-get($title-height, 'sm');
			display: flex;
			align-items: center;

			h1 {
				font-size: map-get($title-size, 'sm');
				font-family: $font-family-text;
				hyphens: auto;
				letter-spacing: unset;
				margin: 0;
			}
		}

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
		.other__content .other__title {
			height: map-get($title-height, 'md');

			h1 {
				font-size: map-get($title-size, 'md');
			}
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'lg')) {
		.other__content .other__title {
			height: map-get($title-height, 'lg');

			h1 {
				font-size: map-get($title-size, 'lg');
			}
		}
	}
</style>
