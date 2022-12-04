<script lang="ts">
	import { page } from '$app/stores';
</script>

<div class="error__wrapper">
	<div class="error">
		<h1>{$page.status}</h1>
		<p>{$page.error?.message}</p>
	</div>
</div>

<style lang="scss">
	.error__wrapper {
		height: 100vh;

		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
