<script lang="ts">
	export let writer: string;
	export let attributes: any;
</script>

<div class="message__wrapper message--{attributes[writer]['position']}">
	<div class="writing__animation">
		<div />
		<span>x</span>
		<div />
		<span>x</span>
		<div />
	</div>
	<svg
		class="message__tip"
		width="25"
		height="21"
		viewBox="0 0 25 21"
		xmlns="http://www.w3.org/2000/svg"
	>
		<path d="M9 0C9 16 1 20 1 20C1 20 9 16 25 16" />
	</svg>
</div>

<style global lang="scss">
	@use '../scss/variables' as *;

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
