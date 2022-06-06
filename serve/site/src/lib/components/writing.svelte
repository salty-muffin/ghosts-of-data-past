<script lang="ts">
	export let writer: string;
	export let attributes: any;
</script>

<div class="writing__wrapper writing--{attributes[writer]['position']}">
	<div class="writing__animation">
		<div />
		<span>x</span>
		<div />
		<span>x</span>
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
		0% {
			opacity: 0;
		}
		30% {
			opacity: 0;
			transform: translateY(80%);
		}
		100% {
			opacity: 1;
			transform: translateY(-20%);
		}
	}

	.writing__animation {
		display: flex;
		align-items: center;
		/* gap: map-get($margin-secondary, 'sm'); */

		div {
			width: map-get($writing-circle-size, 'sm');
			height: map-get($writing-circle-size, 'sm');

			background-color: map-get($colors, 'foreground');
			border-radius: 100%;

			animation-name: fadeInOut;
			animation-duration: 1.6s;
			animation-timing-function: ease;
			animation-iteration-count: infinite;
			animation-direction: alternate;
			animation-fill-mode: both;
		}
		div:nth-of-type(1) {
			animation-delay: 0s;
		}
		div:nth-of-type(2) {
			animation-delay: 0.2s;
		}
		div:nth-of-type(3) {
			animation-delay: 0.4s;
		}

		span {
			visibility: hidden;
			width: map-get($margin-secondary, 'sm');
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
			div {
				border-width: map-get($border-width, 'lg');
			}

			span {
				width: map-get($margin-secondary, 'lg');
			}
		}
	}
</style>
