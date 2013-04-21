-- only add these index after data is loaded:

ALTER TABLE hyg_stars ADD PRIMARY KEY (StarID);
CREATE INDEX hyg_dist_idx ON hyg_stars (Distance);
CREATE INDEX hyg_name_idx ON hyg_stars (ProperName);
