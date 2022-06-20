<script lang="ts">
	import { onMount } from 'svelte';

	import Nav from '$lib/components/nav.svelte';
	import Footer from '$lib/components/footer.svelte';
	import SidenoteColumn from '$lib/components/sidenote-column.svelte';
	import Sidenote from '$lib/components/sidenote.svelte';
	import Marker from '$lib/components/sidenote-marker.svelte';
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
	<div class="about__container">
		<!-- left sidenote column -->
		<SidenoteColumn class="sidenote__left">
			<Sidenote id="1">
				<p>
					Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum
					provident molestiae fuga error tenetur omnis placeat sit, non accusantium maxime
					praesentium, dicta architecto, unde doloremque ab earum.
				</p>
			</Sidenote>
		</SidenoteColumn>

		<!-- main content -->
		<article class="about__content">
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
			<section>
				<p>
					this is a placeholder for the documentation. In the end there might be two or three pages
					descreibing in detail. One may be going over general background stuff, while another will
					be going over technical backgrounds.
				</p>
				<p>
					This here is just filler text, because I assume the introcution would probably be longer,
					but we'll see I guess. Lorem ipsum dolor sit amet consectetur adipisicing elit.
				</p>
			</section>
			<section>
				<h2 id="chapter_1" class="about--breathing">First Chapter</h2>
				<p>
					<i>Lorem ipsum</i> <b>dolor sit</b> <b><i>amet consectetur</i></b> adipisicing elit<Marker
						id="1">1</Marker
					>. Similique qui laboriosam eum provident molestiae fuga error tenetur omnis placeat sit,
					non accusantium maxime praesentium, dicta architecto, unde doloremque ab earum.
				</p>
				<p>
					Lorem ipsum dolor sit amet consectetur adipisicing elit.<Marker id="2">2</Marker> Similique
					qui laboriosam eum provident molestiae fuga error tenetur omnis placeat sit, non accusantium
					maxime praesentium, dicta architecto, unde doloremque ab earum.<Marker id="3">3</Marker>
				</p>
				<Image jpgSrcset={sampleImage} placeholder={sampleImagePlaceholder} alt="test" />
				<p>
					Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum
					provident molestiae fuga error tenetur omnis placeat sit, non accusantium maxime
					praesentium, dicta architecto, unde doloremque ab earum.
				</p>
			</section>
		</article>

		<!-- right sidenote column -->
		<SidenoteColumn class="sidenote__right">
			<Sidenote id="2">
				<p>
					Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum
					provident molestiae fuga error tenetur omnis placeat sit, non accusantium maxime
					praesentium, dicta architecto, unde doloremque ab earum.
				</p>
			</Sidenote>
			<Sidenote id="3" offset={6}>
				<p>
					Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum
					provident molestiae fuga error tenetur omnis placeat sit, non accusantium maxime
					praesentium, dicta architecto, unde doloremque ab earum.
				</p>
			</Sidenote>
		</SidenoteColumn>
	</div>
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

		display: flex;
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

	.about__content {
		flex-shrink: 1;
		max-width: $container-width;
		margin: 0 map-get($margin-primary, 'sm');

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

	.about--breathing {
		font-variation-settings: 'wght' var(--h-weight), 'ital' var(--h-italic);
	}

	@media only screen and (min-width: $breakpoint) {
		.about .nav__wrapper {
			margin: map-get($margin-primary, 'lg') 0;
		}

		.about__content {
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
