<script lang="ts">
	import { onMount } from 'svelte';

	import Nav from '$lib/components/nav.svelte';
	import Footer from '$lib/components/footer.svelte';
	import Sidenote from '$lib/components/sidenote.svelte';
	import Image from '$lib/components/image.svelte';

	// intersection observer for the 'breathing' headers
	let observer: IntersectionObserver | undefined;
	onMount(() => {
		observer = new IntersectionObserver((entries, observer) => {
			entries.forEach(function (entry) {
				// pause/play the animation
				if (entry.isIntersecting) entry.target.classList.add('about--breathing');
				else entry.target.classList.remove('about--breathing');
			});
		});

		const headings = document.getElementsByClassName('about--breathing');
		if (headings)
			Array.from(headings).forEach((element) => {
				observer?.observe(element);
			});

		// remove noscroll
		document.body.classList.remove('chat--noscroll');
	});

	// image imports
	// @ts-ignore
	import sampleImage from '$assets/images/seed0000.jpg?w=375;550;720&jpg&srcset'; // @ts-ignore
	import sampleImagePlaceholder from '$assets/images/seed0000.jpg?w=100&jpg&metadata';
</script>

<svelte:head>
	<title>about</title>
</svelte:head>

<div class="about">
	<article class="about__container">
		<header class="about__header">
			<h1 class="about--breathing">About</h1>
			<Nav links={[{ href: '/', text: 'chat' }]} />
		</header>

		<!-- table of contents -->
		<div class="about__toc">
			<ol>
				<li><a href="#chapter_1">First Chapter</a></li>
				<li>
					<a href="/">Second Chapter</a>
					<ol>
						<li><a href="/">First Subchapter</a></li>
						<li><a href="/">Second Subchapter</a></li>
					</ol>
				</li>
				<li><a href="/">Third Chapter</a></li>
			</ol>
		</div>

		<!-- main content -->

		<p>
			this is a placeholder for the documentation. In the end there might be two or three pages
			descreibing in detail. One may be going over general background stuff, while another will be
			going over technical backgrounds.
		</p>
		<p>
			This here is just filler text, because I assume the introcution would probably be longer, but
			we'll see I guess. Lorem ipsum dolor sit amet consectetur adipisicing elit.
		</p>

		<h2 id="chapter_1" class="about--breathing">First Chapter</h2>
		<p>
			<i>Lorem ipsum</i> <b>dolor sit</b> <b><i>amet consectetur</i></b> adipisicing elit
			<Sidenote id={1}>
				Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum
				provident molestiae fuga error tenetur omnis placeat sit, non accusantium maxime
				praesentium, dicta architecto, unde doloremque ab earum.
			</Sidenote>. Similique qui laboriosam eum provident molestiae fuga error tenetur omnis placeat
			sit, non accusantium maxime praesentium, dicta architecto, unde doloremque ab earum.
		</p>
		<p>
			Lorem ipsum dolor sit amet consectetur adipisicing elit.
			<Sidenote id={2}>
				Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum
				provident molestiae fuga error tenetur omnis placeat sit, non accusantium maxime
				praesentium, dicta architecto, unde doloremque ab earum.
			</Sidenote> Similique qui laboriosam eum provident molestiae fuga error tenetur omnis placeat sit,
			non accusantium maxime praesentium, dicta architecto, unde doloremque ab earum.
			<Sidenote id={3}>
				Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum
				provident molestiae fuga error tenetur omnis placeat sit, non accusantium maxime
				praesentium, dicta architecto, unde doloremque ab earum.
			</Sidenote>
		</p>
		<Image jpgSrcset={sampleImage} placeholder={sampleImagePlaceholder} alt="test" />
		<p>
			Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum
			provident molestiae fuga error tenetur omnis placeat sit, non accusantium maxime praesentium,
			dicta architecto, unde doloremque ab earum.
		</p>
	</article>
	<Footer />
</div>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.about {
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

	.about__header {
		display: flex;
		flex-wrap: wrap;

		h1 {
			flex-grow: 1;
			margin-bottom: 0.5em;
		}
	}

	.about__container {
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

	.about__toc {
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

	.about--breathing {
		font-variation-settings: 'wght' var(--h-weight), 'ital' var(--h-italic);
	}

	@media only screen and (min-width: $breakpoint) {
		.about .nav__wrapper {
			margin: map-get($margin-primary, 'lg') 0;
		}

		.about__container {
			margin: 0 map-get($margin-primary, 'lg');

			img {
				width: 100%;
				margin: 0;
			}
		}

		.about__toc {
			padding: map-get($margin-primary, 'lg');
			margin: 0 2 * map-get($margin-primary, 'lg') map-get($margin-primary, 'lg') 0;
			float: left;

			border: solid map-get($border-width, 'lg') map-get($colors, 'foreground');
		}
	}
</style>
