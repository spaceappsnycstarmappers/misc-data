DROP TABLE hyg_stars;

CREATE TABLE hyg_stars (
	StarID int,
	BayerFlamsteed text,
	ProperName text,
	RA text,
	Dec text,
	Distance decimal,
	PMRA text,
	PMDec text,
	Mag text,
	Spectrum text,
	ColorIndex text,
	X decimal,
	Y decimal,
	Z decimal,
	VX decimal,
	VY decimal,
	VZ decimal
);

-- only add this index after data is loaded:
-- CREATE INDEX ON hyg_stars (Distance);
