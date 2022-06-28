import adapter from '@sveltejs/adapter-static';
import preprocess from 'svelte-preprocess';
import { mdsvex } from 'mdsvex';
import { imagetools } from 'vite-imagetools';
import { resolve } from 'path';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	extensions: ['.svelte', '.svx'],
	// Consult https://github.com/sveltejs/svelte-preprocess
	// for more information about preprocessors
	preprocess: [
		preprocess(),
		mdsvex({
			layout: './src/lib/layouts/doc-layout-wrapper.svelte'
		})
	],

	kit: {
		adapter: adapter(),
		prerender: {
			default: true
		},
		vite: {
			resolve: {
				alias: {
					$assets: resolve('src/assets')
				}
			},
			plugins: [imagetools()]
		}
	}
};

export default config;
