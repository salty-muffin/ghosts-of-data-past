<script lang="ts">
	import { onMount } from 'svelte';

	import { FontAnimator } from '$lib/components/font-animation';
	import { cubicInOut } from 'svelte/easing';

	import Footer from '$lib/components/footer.svelte';

	// intersection observer for the 'breathing' headers
	let observer: IntersectionObserver | undefined;

	// doc wrapper element
	let doc: HTMLElement | undefined;

	// setting up breathing animation parameters & animators
	const duration = 5000;
	const bodyAnimation = new FontAnimator({ weight: 200, italic: 0 }, { weight: 200, italic: 7 });
	let bodyC = bodyAnimation.getStart();
	const quoteAnimation = new FontAnimator({ weight: 200, italic: 5 }, { weight: 200, italic: 12 });
	let quoteC = bodyAnimation.getStart();
	onMount(() => {
		// breathing animation
		let animation = requestAnimationFrame(function update(timestamp: number) {
			// calculation ratio
			const pos = Math.abs(((timestamp % (duration * 2)) - duration) / duration);
			const interpolated = cubicInOut(pos);

			// updating all font animations
			bodyC = bodyAnimation.update(interpolated);
			quoteC = quoteAnimation.update(interpolated);

			// updating css variables
			if (doc) {
				doc.style.setProperty('--b-weight', String(bodyC.weight));
				doc.style.setProperty('--b-italic', String(bodyC.italic));
				doc.style.setProperty('--q-weight', String(quoteC.weight));
				doc.style.setProperty('--q-italic', String(quoteC.italic));
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

		// get all paragraphs by tag
		const paragraphs = Array.from(document.querySelectorAll('p'));

		// observe all paragraphs
		if (paragraphs)
			paragraphs.forEach((element) => {
				observer?.observe(element);
			});

		return () => {
			cancelAnimationFrame(animation);
		};
	});
</script>

<div class="doc" bind:this={doc}>
	<article class="doc__container">
		<main class="doc__content">
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

	div.doc__nav {
		height: unset;
	}

	.doc__nav {
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

	.doc__title {
		font-size: map-get($title-size, 'sm');
	}

	.doc__container {
		flex-grow: 1;

		width: min(calc(100vw - 2 * map-get($margin-primary, 'sm')), map-get($container-width, 'sm'));
		// margin: 0 map-get($margin-primary, 'sm');
	}

	@function encodecolor($string) {
		@if type-of($string) == 'color' {
			$hex: str-slice(ie-hex-str($string), 4);
			$string: unquote('#{$hex}');
		}
		$string: '%23' + $string;
		@return $string;
	}

	.doc__content {
		// font-feature-settings: 'ss01' 1;

		p:first-of-type {
			margin-top: 0;
		}

		li > p {
			margin: 0;
		}

		ul {
			list-style: none;
			margin-left: 0;
			padding-left: 0;

			li {
				padding-left: 1em;
				text-indent: -1em;
			}

			li:before {
				background-image: url("data:image/svg+xml,%3Csvg%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cpath%20d%3D%22M8.34559%200.5C0.500011%205.85477%200.499977%2012.9945%203.1152%2018.3492C6.5%2023.5%2010.8832%2025.8335%2019.6781%2020C27.2565%2014.9734%2021.3432%2011%2019.6781%206.74723C18.013%202.49447%2010.5%207.52176%207.47386%206.74723C3.14174%205.63845%201.66231%203.47487%200.5%201.39246%22%20stroke%3D%22#{encodecolor(map-get($colors, 'foreground'))}%22%20stroke-width%3D%222%22%2F%3E%3C%2Fsvg%3E%0A");
				background-repeat: no-repeat;
				background-position: left center;
				background-size: 0.5em;
				content: '';
				padding-left: 24px;
				padding-right: 5px;

				stroke: map-get($colors, 'foreground');
			}
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

		.image-component {
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

	.blockquote.doc--breathing {
		font-variation-settings: 'wght' var(--q-weight), 'ital' var(--q-italic);
	}

	@media only screen and (min-width: $sidenote-breakpoint) {
		.doc__nav {
			float: left;

			width: 18em;
			margin-left: calc(-18em - 2 * map-get($margin-primary, 'lg'));

			.nav__links {
				flex-direction: column;
				align-items: flex-end;
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
		.doc__title {
			margin: 1.5em 0;

			font-size: map-get($title-size, 'md');
		}

		.doc__container {
			width: min(calc(100vw - 2 * map-get($margin-primary, 'md')), map-get($container-width, 'md'));
			// margin: 0 map-get($margin-primary, 'lg');
		}

		.doc__content .image-component {
			width: 100%;
			margin: 0;

			&.doc__logo {
				width: min(100%, 16em);
				float: right;
				clear: right;
				margin: 0 0 map-get($margin-primary, 'md') map-get($margin-primary, 'md');

				/* filter: drop-shadow(0 0 map-get($margin-secondary, 'lg') map-get($colors, 'foreground'))
					drop-shadow(0 0 map-get($margin-primary, 'lg') map-get($colors, 'foreground'))
					drop-shadow(0 0 map-get($border-blur, 'lg') map-get($colors, 'foreground')); */
			}
		}

		.doc__toc {
			padding: map-get($margin-primary, 'md');
			margin: 0 2 * map-get($margin-primary, 'sm') map-get($margin-primary, 'md') 0;
			float: left;

			border: solid map-get($border-width, 'md') map-get($colors, 'foreground');
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'lg')) {
		.doc__title {
			margin: 1.5em 0;

			font-size: map-get($title-size, 'lg');
		}

		.doc__container {
			width: min(calc(100vw - 2 * map-get($margin-primary, 'lg')), map-get($container-width, 'lg'));
			// margin: 0 map-get($margin-primary, 'lg');
		}

		.doc__content .image-component {
			width: 100%;
			margin: 0;

			&.doc__logo {
				width: min(100%, 16em);
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
