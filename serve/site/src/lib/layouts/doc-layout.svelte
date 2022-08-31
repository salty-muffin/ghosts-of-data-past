<script lang="ts">
	import type { Link } from '$lib/components/nav.svelte';
	export let title = '';
	export let links: Link[] = [];

	import { onMount } from 'svelte';

	import { FontAnimator } from '$lib/components/font-animation';
	import { cubicInOut } from 'svelte/easing';

	import Nav from '$lib/components/nav.svelte';
	import Footer from '$lib/components/footer.svelte';

	// intersection observer for the 'breathing' headers
	let observer: IntersectionObserver | undefined;

	// doc wrapper element
	let doc: HTMLElement | undefined;

	// setting up breathing animation parameters & animators
	const duration = 5000;
	const bodyAnimation = new FontAnimator({ weight: 200, italic: 0 }, { weight: 200, italic: 7 });
	let bodyC = bodyAnimation.getStart();
	onMount(() => {
		// breathing animation
		let animation = requestAnimationFrame(function update(timestamp: number) {
			// calculation ratio
			const pos = Math.abs(((timestamp % (duration * 2)) - duration) / duration);
			const interpolated = cubicInOut(pos);

			// updating all font animations
			bodyC = bodyAnimation.update(interpolated);

			// updating css variables
			if (doc) {
				doc.style.setProperty('--b-weight', String(bodyC.weight));
				doc.style.setProperty('--b-italic', String(bodyC.italic));
			}

			// append next animation frame
			animation = requestAnimationFrame(update);
		});

		// only animate when in view
		observer = new IntersectionObserver((entries, observer) => {
			entries.forEach(function (entry) {
				// pause/play the animation
				if (entry.isIntersecting) entry.target.classList.add('doc--breathing');
				else entry.target.classList.remove('doc--breathing');
			});
		});

		// get all headers by tag
		const headings = Array.from(document.querySelectorAll('p'));

		// observe all headers
		if (headings)
			headings.forEach((element) => {
				observer?.observe(element);
			});

		// remove noscroll
		document.body.classList.remove('chat--noscroll');

		return () => {
			cancelAnimationFrame(animation);
		};
	});
</script>

<svelte:head>
	<title>{title}</title>
</svelte:head>

<div class="doc" bind:this={doc}>
	<article class="doc__container">
		<h1 class="doc__title">{title}</h1>

		<main class="doc__content">
			<Nav class="doc__nav" {links} />
			<slot />
		</main>
	</article>
	<Footer />
</div>

<style global lang="scss">
	@use '../../lib/scss/variables' as *;

	.doc {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: center;
		min-height: 100vh;
	}

	.doc__nav {
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
				}
			}
		}
	}

	.doc__title {
		font-size: map-get($title-size, 'sm');
	}

	.doc__container {
		flex-grow: 1;

		max-width: $container-width;
		margin: 0 map-get($margin-primary, 'sm');
	}

	.doc__content {
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

			text-align: right;
			margin-top: 1.5em;
		}

		h1,
		h2 {
			&::after {
				display: block;
				content: '';
				border-top: 1px solid map-get($colors, 'foreground');
				width: 100%;
			}
		}

		.image {
			width: calc(100% + 2 * map-get($margin-primary, 'sm'));
			margin: 0 0 - map-get($margin-primary, 'sm');

			&.doc__logo {
				width: 100%;
				margin: 0 0 map-get($margin-primary, 'sm') 0;

				filter: drop-shadow(0 0 map-get($margin-secondary, 'sm') map-get($colors, 'foreground'))
					drop-shadow(0 0 map-get($margin-primary, 'sm') map-get($colors, 'foreground'))
					drop-shadow(0 0 map-get($border-blur, 'sm') map-get($colors, 'foreground'));
			}
		}
	}

	.doc__toc {
		padding: map-get($margin-primary, 'sm');
		margin: 0 0 map-get($margin-primary, 'sm') 0;

		border: solid map-get($border-width, 'sm') map-get($colors, 'foreground');

		& > ol {
			padding: 0;
		}
		ol {
			margin: 0;

			counter-reset: item;
		}
		li {
			display: block;
		}
		li:before {
			content: counters(item, '.') ' ';
			counter-increment: item;
		}
	}

	.doc--breathing {
		font-variation-settings: 'wght' var(--b-weight), 'ital' var(--b-italic);
	}

	@media only screen and (min-width: $sidenote-breakpoint) {
		.doc__nav {
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
						display: block;
						content: '';
						margin-left: unset;
						margin-top: map-get($margin-primary, 'lg');
						border-left: unset;
						border-top: 1px solid map-get($colors, 'foreground');
						width: 100%;
					}
				}

				h4 {
					text-align: right;
				}
			}
		}
	}

	@media only screen and (min-width: $breakpoint) {
		.doc__title {
			margin: 1.5em 0;

			font-size: map-get($title-size, 'lg');
		}

		.doc__container {
			margin: 0 map-get($margin-primary, 'lg');
		}

		.doc__content .image {
			width: 100%;
			margin: 0;

			&.doc__logo {
				width: min(100%, 20em);
				float: right;
				clear: right;
				margin: 0 0 map-get($margin-primary, 'lg') map-get($margin-primary, 'lg');

				/* filter: drop-shadow(0 0 map-get($margin-secondary, 'lg') map-get($colors, 'foreground'))
					drop-shadow(0 0 map-get($margin-primary, 'lg') map-get($colors, 'foreground'))
					drop-shadow(0 0 map-get($border-blur, 'lg') map-get($colors, 'foreground')); */
			}
		}

		.doc__toc {
			padding: map-get($margin-primary, 'lg');
			margin: 0 2 * map-get($margin-primary, 'sm') map-get($margin-primary, 'lg') 0;
			float: left;

			border: solid map-get($border-width, 'lg') map-get($colors, 'foreground');
		}
	}
</style>
