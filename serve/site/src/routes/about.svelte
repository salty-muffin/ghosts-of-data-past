<svelte:head>
	<title>about</title>
</svelte:head>

<div class="about">
	<h1>About</h1>
	<p>this is a placeholder for the documentation</p>
	<p><a href="/">back to chat</a></p>
	<p>
		Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum provident
		molestiae fuga error tenetur omnis placeat sit, non accusantium maxime praesentium, dicta
		architecto, unde doloremque ab earum.
	</p>
	<p>
		Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum provident
		molestiae fuga error tenetur omnis placeat sit, non accusantium maxime praesentium, dicta
		architecto, unde doloremque ab earum.
	</p>
	<img src="seed0000.jpg" alt="test" />
	<p>
		Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique qui laboriosam eum provident
		molestiae fuga error tenetur omnis placeat sit, non accusantium maxime praesentium, dicta
		architecto, unde doloremque ab earum.
	</p>
</div>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.about {
		max-width: $container-width;
		margin: auto;

		padding: map-get($margin-primary, 'sm');

		img {
			max-width: 100%;
			height: auto;
		}
	}

	@media only screen and (min-width: $breakpoint) {
		.about {
			padding: map-get($margin-primary, 'lg');
		}
	}
</style>
