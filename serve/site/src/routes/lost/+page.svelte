<script lang="ts">
	import { onMount } from 'svelte';

	import { FontAnimator } from '$lib/components/font-animation';
	import { cubicInOut } from 'svelte/easing';

	import Footer from '$lib/components/footer.svelte';

	// lost wrapper element
	let lost: HTMLElement | undefined;

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
			if (lost) {
				lost.style.setProperty('--b-weight', String(bodyC.weight));
				lost.style.setProperty('--b-italic', String(bodyC.italic));
			}

			// append next animation frame
			animation = requestAnimationFrame(update);
		});

		return () => {
			cancelAnimationFrame(animation);
		};
	});
</script>

<svelte:head>
	<title>ghosts of data past</title>
</svelte:head>

<div class="lost" bind:this={lost}>
	<div class="lost__container">
		<h1 class="lost__title">connection lost</h1>

		<main class="lost__content">
			<p>
				It appears that your link to the afterworld of data has expired. Links from the exhibition
				are only valid for on the day they were made.
			</p>
			<p>
				You may still see a documentation of the work and read all texts associated with it at <a
					href="https://ghostsonthe.net">ghostsonthe.net</a
				>
			</p>
		</main>
	</div>
	<Footer />
</div>

<style global lang="scss">
	@use '../../lib/scss/variables' as *;

	.lost {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: center;
		min-height: 100vh;
	}

	.lost__title {
		font-size: map-get($title-size, 'sm');
	}

	.lost__container {
		flex-grow: 1;

		width: min(calc(100vw - 2 * map-get($margin-primary, 'sm')), map-get($container-width, 'sm'));
		// margin: 0 map-get($margin-primary, 'sm');
	}

	.lost__content {
		// font-feature-settings: 'ss01' 1;

		p:first-of-type {
			margin-top: 0;
		}

		p {
			font-variation-settings: 'wght' var(--b-weight), 'ital' var(--b-italic);
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'md')) {
		.lost__title {
			margin: 1.5em 0;

			font-size: map-get($title-size, 'md');
		}

		.lost__container {
			width: min(calc(100vw - 2 * map-get($margin-primary, 'md')), map-get($container-width, 'md'));
			// margin: 0 map-get($margin-primary, 'lg');
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'lg')) {
		.lost__title {
			margin: 1.5em 0;

			font-size: map-get($title-size, 'lg');
		}

		.lost__container {
			width: min(calc(100vw - 2 * map-get($margin-primary, 'lg')), map-get($container-width, 'lg'));
			// margin: 0 map-get($margin-primary, 'lg');
		}
	}
</style>
