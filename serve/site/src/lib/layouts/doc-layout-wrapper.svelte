<script>
	// @ts-nocheck
	export let title = '';
	export let links = [];

	import Layout from './doc-layout.svelte';
</script>

<Layout {title} {links}><slot /></Layout>
