import adapter from '@sveltejs/adapter-static';
import preprocess from 'svelte-preprocess';
import { imagetools } from 'vite-imagetools';
import path from 'path';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://github.com/sveltejs/svelte-preprocess
	// for more information about preprocessors
	preprocess: preprocess(),

	kit: {
		adapter: adapter(),
		prerender: {
			default: true
		},
		vite: {
			resolve: {
				alias: {
					$assets: path.resolve('src/assets')
				}
			},
			plugins: [imagetools()]
		}
	}
};

export default config;