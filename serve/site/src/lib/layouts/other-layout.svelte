<script lang="ts">
	import MuteButton from '$lib/components/mute-button.svelte';

	import type { Link } from '$lib/components/nav.svelte';

	export let title = '';
	export let links: Link[] = [];

	import Nav from '$lib/components/nav.svelte';
	import Footer from '$lib/components/footer.svelte';
</script>

<svelte:head>
	<title>{title}</title>
</svelte:head>

<div class="other">
	<article class="other__container">
		<h1 class="other__title">{title}</h1>

		<main class="other__content">
			<Nav class="other__nav" {links}>
				<MuteButton>
					<h4 slot="muted">unmute</h4>
					<h4 slot="unmuted">mute</h4>
				</MuteButton>
			</Nav>
			<slot />
		</main>
	</article>
	<Footer />
</div>

<style global lang="scss">
	@use '../../lib/scss/variables' as *;

	.other {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: center;
		min-height: 100vh;
	}

	.other__nav {
		height: unset;
		margin-bottom: map-get($margin-primary, 'sm');
		.nav__links {
			margin: 0;
			gap: map-get($margin-primary, 'sm');

			button {
				display: flex;

				&::after {
					display: block;
					content: '';
					margin-left: map-get($margin-primary, 'sm');
					border-right: 1px solid map-get($colors, 'foreground');
					width: 100%;
					height: 100%;
				}
			}
		}
	}

	.other__title {
		font-size: map-get($title-size, 'sm');
		font-family: $font-family-text;
		hyphens: auto;
		letter-spacing: unset;
	}

	.other__container {
		flex-grow: 1;

		width: min(calc(100vw - 2 * map-get($margin-primary, 'sm')), map-get($container-width, 'sm'));
		// margin: 0 map-get($margin-primary, 'sm');
	}

	.other__content {
		font-feature-settings: 'ss01' 1;

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

	@media only screen and (min-width: $sidenote-breakpoint) {
		.other__nav {
			float: left;

			width: 10em;
			margin-left: calc(-10em - 2 * map-get($margin-primary, 'lg'));

			.nav__links {
				flex-direction: column;
				gap: map-get($margin-primary, 'lg');
				margin: 0;

				button {
					display: unset;

					&::after {
						margin-left: unset;
						margin-top: map-get($margin-primary, 'lg');
						border-left: unset;
						border-top: 1px solid map-get($colors, 'foreground');
					}
				}

				h4 {
					text-align: right;
				}
			}
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'md')) {
		.other__title {
			margin: 1.5em 0;

			font-size: map-get($title-size, 'md');
		}

		.other__container {
			width: min(calc(100vw - 2 * map-get($margin-primary, 'md')), map-get($container-width, 'md'));
			// margin: 0 map-get($margin-primary, 'lg');
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'lg')) {
		.other__title {
			margin: 1.5em 0;

			font-size: map-get($title-size, 'lg');
		}

		.other__container {
			width: min(calc(100vw - 2 * map-get($margin-primary, 'lg')), map-get($container-width, 'lg'));
			// margin: 0 map-get($margin-primary, 'lg');
		}
	}
</style>
