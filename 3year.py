import xlrd
from Bio import SeqIO

def main():
	vids_file = 'vids_lab_codes.xlsx'
	fasta_file = 'g__Dorea.fasta'
	out_file = 'g__Dorea253_3yr.fasta'

	book = xlrd.open_workbook(vids_file)
	sheet = book.sheet_by_name('Sheet2')
	data = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	ids = [i[1] for i in data]
	ids.pop(0)
	ids = [i.split('.')[1] for i in ids]
	ids = [i.encode('UTF8') for i in ids]
	ids = ["S.%s" % (i) for i in ids]
	f = open(out_file, 'w')

	filter_passed = []
	for seq_record in SeqIO.parse(fasta_file, "fasta"):
		groups = seq_record.id.replace('_','-').split('-')		
		test_id = '-'.join([groups[i] for i in [0,1,4]])
		test_id = test_id.replace('-','.',1)
		test_id = test_id.replace('-','_',1)
		for i in range(0,len(ids)):
			if test_id == ids[i]:
				filter_passed.append(seq_record)
				print seq_record.format("fasta")
	SeqIO.write(filter_passed, out_file, "fasta")

if __name__ == "__main__":
	main()

