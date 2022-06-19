<script lang="ts">
	import Footer from '$lib/components/footer.svelte';
	import SidenoteColumn from '$lib/components/sidenote-column.svelte';
	import Sidenote from '$lib/components/sidenote.svelte';
	import Marker from '$lib/components/sidenote-marker.svelte';

	let marker1: Element | undefined;
	let marker2: Element | undefined;
</script>

<svelte:head>
	<title>about</title>
</svelte:head>

<div class="about">
	<div class="about__container">
		<SidenoteColumn class="sidenote__left">
			<Sidenote id="1">
				<p>
					Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum
					provident molestiae fuga error tenetur omnis placeat sit, non accusantium maxime
					praesentium, dicta architecto, unde doloremque ab earum.
				</p>
			</Sidenote>
		</SidenoteColumn>

		<div class="about__content">
			<h1>About</h1>
			<p>this is a placeholder for the documentation</p>
			<p><a href="/">back to chat</a></p>
			<div class="about__toc">
				<ol>
					<li>First Chapter</li>
					<li>
						Second Chapter
						<ol>
							<li>First Subchapter</li>
							<li>Second Subchapter</li>
						</ol>
					</li>
					<li>Third Chapter</li>
				</ol>
			</div>
			<p>
				Lorem ipsum dolor sit amet consectetur adipisicing elit<Marker id="1">1</Marker>. Similique
				qui laboriosam eum provident molestiae fuga error tenetur omnis placeat sit, non accusantium
				maxime praesentium, dicta architecto, unde doloremque ab earum.
			</p>
			<p>
				Lorem ipsum dolor sit amet consectetur adipisicing elit.<Marker id="2">2</Marker> Similique qui
				laboriosam eum provident molestiae fuga error tenetur omnis placeat sit, non accusantium maxime
				praesentium, dicta architecto, unde doloremque ab earum.<Marker id="3">3</Marker>
			</p>
			<img src="seed0000.jpg" alt="test" />
			<p>
				Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum
				provident molestiae fuga error tenetur omnis placeat sit, non accusantium maxime
				praesentium, dicta architecto, unde doloremque ab earum.
			</p>
		</div>

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
	}

	.about__container {
		flex-grow: 1;

		display: flex;
	}

	.about__toc {
		padding: map-get($margin-primary, 'sm');
		margin: 0 map-get($margin-primary, 'sm') 0 0;
		float: left;

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
			max-width: calc(100% + 2 * map-get($margin-primary, 'sm'));
			height: auto;
			margin: 0 0 - map-get($margin-primary, 'sm');
		}
	}

	@media only screen and (min-width: $breakpoint) {
		.about__content {
			margin: 0 map-get($margin-primary, 'lg');

			img {
				max-width: 100%;
				margin: 0;
			}
		}
	}
</style>
