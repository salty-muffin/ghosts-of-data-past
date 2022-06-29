import adapter from '@sveltejs/adapter-static';
import preprocess from 'svelte-preprocess';
import path from 'path';
import { fileURLToPath } from 'url';
import { imagetools } from 'vite-imagetools';
import { mdsvex } from 'mdsvex';

// rehype plugins
import rehypeSlug from 'rehype-slug';
import rehypeTOC from '@jsdevtools/rehype-toc';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	extensions: ['.svelte', '.svx'],
	// Consult https://github.com/sveltejs/svelte-preprocess
	// for more information about preprocessors
	preprocess: [
		preprocess(),
		mdsvex({
			layout: path.join(
				path.dirname(fileURLToPath(import.meta.url)),
				'src/lib/layouts/doc-layout-wrapper.svelte'
			),
			rehypePlugins: [
				rehypeSlug,
				[
					rehypeTOC,
					{ headings: ['h1', 'h2'], cssClasses: { toc: 'doc__toc' }, position: 'beforebegin' }
				]
			]
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
					$assets: path.resolve('src/assets')
				}
			},
			plugins: [imagetools()]
		}
	}
};

export default config;
