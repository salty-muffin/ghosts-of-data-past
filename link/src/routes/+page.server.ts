export const prerender = true;

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
		let domain = 'http://localhost:5000';
		if ('DOMAIN' in env && env.DOMAIN) {
			domain = env.DOMAIN;
		}

		let qrData = '';
		qr.toString(
			`${domain}/?gate=${gate}`,
			{ type: 'svg', errorCorrectionLevel: 'Q' },
			(err, data) => {
				if (data) {
					qrData = data;
				}
				if (err) {
					throw error(500, `could not create qr code: ${err}`);
				}
			}
		);

		return {
			gate: gate,
			domain: domain,
			qr: qrData
		};
	} catch (err) {
		throw error(500, `could not open text file: ${err}`);
	}
};
