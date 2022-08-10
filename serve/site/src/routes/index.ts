import chat from '$lib/data/chat-attributes.json';
import settings from '$lib/data/settings.json';

export const GET = async () => {
	if (chat && settings) {
		return {
			body: { chatAttributes: chat, settings: settings }
		};
	}

	return {
		status: 404
	};
};
