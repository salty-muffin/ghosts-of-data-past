<script lang="ts">
	import Footer from '$lib/components/footer.svelte';
</script>

<svelte:head>
	<title>about</title>
</svelte:head>

<div class="about__center">
	<div class="about">
		<div class="about__content">
			<h1>About</h1>
			<p>this is a placeholder for the documentation</p>
			<p><a href="/">back to chat</a></p>
			<p>
				Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum
				provident molestiae fuga error tenetur omnis placeat sit, non accusantium maxime
				praesentium, dicta architecto, unde doloremque ab earum.
			</p>
			<p>
				Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum
				provident molestiae fuga error tenetur omnis placeat sit, non accusantium maxime
				praesentium, dicta architecto, unde doloremque ab earum.
			</p>
			<img src="seed0000.jpg" alt="test" />
			<p>
				Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum
				provident molestiae fuga error tenetur omnis placeat sit, non accusantium maxime
				praesentium, dicta architecto, unde doloremque ab earum.
			</p>
		</div>
		<Footer />
	</div>
</div>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.about__center {
		display: flex;
		justify-content: center;
		min-height: 100vh;
	}

	.about {
		display: flex;
		flex-direction: column;

		max-width: $container-width;
		margin: 0 map-get($margin-primary, 'sm');
	}

	.about__content {
		flex-grow: 1;

		img {
			max-width: calc(100% + 2 * map-get($margin-primary, 'sm'));
			height: auto;
			margin: 0 0 - map-get($margin-primary, 'sm');
		}
	}

	@media only screen and (min-width: $breakpoint) {
		.about {
			margin: 0 map-get($margin-primary, 'lg');
		}

		.about__content {
			img {
				max-width: 100%;
				margin: 0;
			}
		}
	}
</style>
