import type { LayoutServerLoad } from './$types';
import { error } from '@sveltejs/kit';
import chat from '$lib/data/chat-attributes.json' assert { type: 'json' };
import settings from '$lib/data/settings.json' assert { type: 'json' };

export const load: LayoutServerLoad = async () => {
	console.log(`[info] processing json src/lib/data/chat-attributes.json`);
	console.log(`[info] processing json src/lib/data/settings.json`);

	if (chat && settings) {
		return {
			chat,
			settings
		};
	}
	throw error(500, 'something wrong with the json files');
};
