<script lang="ts">
	export let imageData: ArrayBuffer;
	export let text: string;

	const arrayBufferView = new Uint8Array(imageData);
	const blob = new Blob([arrayBufferView], { type: 'image/jpeg' });

	const img_url = URL.createObjectURL(blob);
</script>

<img src={img_url} alt={text} />
