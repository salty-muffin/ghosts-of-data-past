<script lang="ts">
	let className = '';
	export { className as class };
</script>

<div class="nav__wrapper {className}"><nav class="nav__links"><a href="/about">about</a></nav></div>

<style global lang="scss">
	@use '../scss/variables' as *;

	.nav__wrapper {
		height: 3em;

		border-top: 1px solid map-get($colors, 'foreground');

		display: flex;
		align-items: center;
	}

	.nav__links {
		width: 100%;
		margin: 0 1em;

		display: flex;
		justify-content: flex-end;
	}
</style>
