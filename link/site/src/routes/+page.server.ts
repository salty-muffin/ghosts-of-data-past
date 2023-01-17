import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import qr from 'qrcode';

export const load: PageServerLoad = async () => {
	try {
		let gate: string | undefined = undefined;
		if ('GATE' in env) {
			gate = env.GATE;
		}

		let qrData = '';
		qr.toString(`http://192.168.178.22:5000/?gate=${gate}`, { type: 'svg' }, (err, data) => {
			if (data) {
				qrData = data;
			}
			if (err) {
				throw error(500, `could not create qr code: ${err}`);
			}
		});

		return {
			gate: gate,
			qr: qrData
		};
	} catch (err) {
		throw error(500, `could not open text file: ${err}`);
	}
};
