import data from '$lib/data/chat-attributes.json';

export const get = async () => {
	if (data) {
		return {
			body: { chatAttributes: data }
		};
	}

	return {
		status: 404
	};
};
