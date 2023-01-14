import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import qr from 'qrcode';

export const load: PageServerLoad = async () => {
	try {
		const id = fs.readFileSync(
			path.join(path.dirname(fileURLToPath(import.meta.url)), '../../../id.txt'),
			'utf8'
		);

		let qrData = '';
		qr.toString(`http://192.168.178.22:5000/${id}`, { type: 'svg' }, (err, data) => {
			if (data) {
				qrData = data;
			}
			if (err) {
				throw error(500, `could not create qr code: ${err}`);
			}
		});

		if (id) {
			return {
				id: id,
				qr: qrData
			};
		}

		throw error(500, 'something wrong with the text file');
	} catch (err) {
		throw error(500, `could not open text file: ${err}`);
	}
};
