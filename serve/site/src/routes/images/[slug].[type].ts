import sharp from 'sharp';

interface Params {
	params: {
		slug: string;
		type: string;
	};
}

export const GET = async ({ params }: Params) => {
	const image = sharp(`src/images/${params.slug}.${params.type}`);

	console.log(`[info] processing src/images/${params.slug}.${params.type}`);

	if (image) {
		return {
			headers: {
				'Content-Type': `image/${(await image.metadata()).format}`
			},
			body: await image.toBuffer()
		};
	}

	return {
		status: 404,
		body: {}
	};
};
