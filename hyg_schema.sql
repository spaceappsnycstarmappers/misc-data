CREATE TABLE hyg_stars (
	StarID int PRIMARY KEY,
	BayerFlamsteed text,
	ProperName text,
	RA text,
	Dec text,
	Distance int,
	PMRA text,
	PMDec text,
	Mag decimal,
	Spectrum text,
	ColorIndex decimal,
	X decimal,
	Y decimal,
	Z decimal,
	VX decimal,
	VY decimal,
	VZ decimal
);

-- only add this index after data is loaded:
-- CREATE INDEX ON hyg_stars (Distance);
