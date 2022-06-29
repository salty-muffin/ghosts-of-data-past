<script lang="ts">
	import type { Link } from '$lib/components/nav.svelte';
	export let title = '';
	export let links: Link[] = [];

	import { onMount } from 'svelte';

	import Nav from '$lib/components/nav.svelte';
	import Footer from '$lib/components/footer.svelte';

	// intersection observer for the 'breathing' headers
	let observer: IntersectionObserver | undefined;
	onMount(() => {
		// only animate when in view
		observer = new IntersectionObserver((entries, observer) => {
			entries.forEach(function (entry) {
				// pause/play the animation
				if (entry.isIntersecting) entry.target.classList.add('doc--breathing');
				else entry.target.classList.remove('doc--breathing');
			});
		});

		// get all headers by tag
		const headings = Array.from(document.querySelectorAll('h1, h2, h3'));

		// observe all headers
		if (headings)
			headings.forEach((element) => {
				observer?.observe(element);
			});

		// remove noscroll
		document.body.classList.remove('chat--noscroll');
	});
</script>

<svelte:head>
	<title>{title}</title>
</svelte:head>

<div class="doc">
	<article class="doc__container">
		<header class="doc__header">
			<h1>{title}</h1>
			<Nav {links} />
		</header>

		<main>
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

		.nav__wrapper {
			height: unset;
			margin: 0 0 map-get($margin-primary, 'sm') 0;
			flex-grow: 1;
		}
		.nav__links {
			margin: 0;
		}
	}

	.doc__header {
		display: flex;
		flex-wrap: wrap;

		h1 {
			flex-grow: 1;
			margin-bottom: 0.5em;

			font-size: map-get($title-size, 'sm');
		}
	}

	.doc__container {
		flex-grow: 1;

		max-width: $container-width;
		margin: 0 map-get($margin-primary, 'sm');

		p:first-of-type {
			margin-top: 0;
		}

		img {
			width: calc(100% + 2 * map-get($margin-primary, 'sm'));
			height: auto;
			margin: 0 0 - map-get($margin-primary, 'sm');
		}

		h1,
		h2,
		h3 {
			scroll-margin-top: 0.5em;
		}

		& > section > *:first-child {
			margin-top: 0;
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
		font-variation-settings: 'wght' var(--h-weight), 'ital' var(--h-italic);
	}

	@media only screen and (min-width: $breakpoint) {
		.about .nav__wrapper {
			margin: map-get($margin-primary, 'lg') 0;
		}

		.doc__header h1 {
			font-size: map-get($title-size, 'lg');
		}

		.doc__container {
			margin: 0 map-get($margin-primary, 'lg');

			img {
				width: 100%;
				margin: 0;
			}
		}

		.doc__toc {
			padding: map-get($margin-primary, 'lg');
			margin: 0 2 * map-get($margin-primary, 'lg') map-get($margin-primary, 'lg') 0;
			float: left;

			border: solid map-get($border-width, 'lg') map-get($colors, 'foreground');
		}
	}
</style>
