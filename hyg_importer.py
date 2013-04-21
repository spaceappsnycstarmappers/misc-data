import csv

def sql_statement_for_rows(headers, rows):
	value_list = ""
	for row in rows:
		row[2] = row[2].replace("'", "")
		row_list = ",".join([('NULL' if x == '' else ("'" + x + "'")) for x in row])
		if value_list != "":
			value_list += ","
		value_list += "(" + row_list + ")"
	header_list = ",".join(headers)
	return "INSERT INTO hyg_stars (%s) VALUES %s;" % (header_list, value_list)

with open('hygxyz_modified.csv', 'rb') as csvfile:
	csvreader = csv.reader(csvfile)
	batch_rows = []
	headers = None
	for row in csvreader:
		if headers is None:
			headers = row # move on
		elif row[5] != "10000000": # distance
			batch_rows.append(row)
			if len(batch_rows) > 100:
				print sql_statement_for_rows(headers, batch_rows)
				batch_rows = []
	print sql_statement_for_rows(headers, batch_rows)
