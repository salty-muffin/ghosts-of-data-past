<script lang="ts">
	export let writer: string;
	export let attributes: any;
</script>

<div class="writing__wrapper writing--{attributes[writer]['position']}">
	<div class="writing__animation">
		<div />
		<div />
		<div />
	</div>
</div>

<style lang="scss">
	@use '../scss/variables' as *;

	.writing__wrapper {
		border: map-get($border-width, 'sm') solid map-get($colors, 'foreground');
		border-radius: map-get($margin-primary, 'sm');

		margin: 0 map-get($margin-secondary, 'sm') map-get($margin-primary, 'sm');
		padding: map-get($margin-secondary, 'sm') map-get($margin-primary, 'sm');
	}
	.writing--left {
		align-self: flex-start;
	}
	.writing--right {
		align-self: flex-end;
	}

	@keyframes fadeInOut {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	.writing__animation {
		display: flex;
		gap: map-get($margin-secondary, 'sm');

		div {
			width: map-get($text-size, 'sm');
			height: map-get($text-size, 'sm');

			border: map-get($border-width, 'sm') solid map-get($colors, 'foreground');
			border-radius: 100%;

			animation-name: fadeInOut;
			animation-duration: 1s;
			animation-timing-function: linear;
			animation-iteration-count: infinite;
			animation-direction: alternate;
			animation-fill-mode: both;
		}
		div:nth-child(1) {
			animation-delay: 0s;
		}
		div:nth-child(2) {
			animation-delay: 0.5s;
		}
		div:nth-child(3) {
			animation-delay: 1s;
		}
	}

	@media only screen and (min-width: $breakpoint) {
		.writing__wrapper {
			border-width: map-get($border-width, 'lg');
			border-radius: map-get($margin-primary, 'lg');

			margin: 0 map-get($margin-secondary, 'lg') map-get($margin-primary, 'lg');
			padding: map-get($margin-secondary, 'lg') map-get($margin-primary, 'lg');
		}

		.writing__animation {
			gap: map-get($margin-secondary, 'lg');

			div {
				border-width: map-get($border-width, 'lg');
			}
		}
	}
</style>
