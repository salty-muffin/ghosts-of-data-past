export const prerender = true;

import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';
import qr from 'qrcode';

export const load: PageServerLoad = async () => {
	try {
		let gate: string | undefined = undefined;
		if ('GATE' in process.env) {
			gate = process.env.GATE;
		}
		let domain = 'http://localhost:5000';
		if ('DOMAIN' in process.env && process.env.DOMAIN) {
			domain = process.env.DOMAIN;
		}

		return {
			gate: gate,
			domain: domain,
			qr: await qr.toDataURL(`${domain}/?gate=${gate}`, {
				type: 'image/png',
				errorCorrectionLevel: 'Q',
				color: { dark: '#ffffffff', light: '#00000000' },
				width: 500
			})
		};
	} catch (err) {
		throw error(500, `could not open text file: ${err}`);
	}
};
