import { sveltekit } from '@sveltejs/kit/vite';
import { imagetools } from 'vite-imagetools';
import path from 'path';

/** @type {import('vite').UserConfig} */
const config = {
	resolve: {
		alias: {
			$assets: path.resolve('src/assets')
		}
	},
	plugins: [sveltekit(), imagetools()]
};

export default config;
