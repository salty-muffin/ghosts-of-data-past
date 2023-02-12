// types
interface FontVariation {
	weight: number;
	italic: number;
}

// functions
const mapInterpolation = (start: number, end: number, fraction: number) => {
	return Math.trunc((end - start) * fraction + start);
};

// classes
export class FontAnimator {
	start: FontVariation;
	end: FontVariation;
	current: FontVariation;

	constructor(start: FontVariation, end: FontVariation) {
		this.start = start;
		this.end = end;
		this.current = start;
	}

	getStart(): FontVariation {
		return this.start;
	}

	update(fraction: number): FontVariation {
		return {
			weight: mapInterpolation(this.start.weight, this.end.weight, fraction),
			italic: mapInterpolation(this.start.italic, this.end.italic, fraction)
		};
	}
}
