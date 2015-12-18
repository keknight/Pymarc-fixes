import pymarc
from pymarc import MARCReader, Record, Field
import datetime
import re 

reader = MARCReader(open('aleph.mrc'))

marc_recs_out = open('newaleph.mrc', 'w')



for record in reader:

	new_marc_rec = Record()

	curr_date = datetime.date.today()
	yy = str(curr_date.year)[2:].zfill(2)
	mm = str(curr_date.month).zfill(2)
	dd = str(curr_date.day).zfill(2)
	entered = yy+mm+dd
	dtst = 's'
	date = record['260']['c']
	dateMatch = re.match('\d{4}', date) #regex to match digits only and get rid of EOL punctuation
	dateStrip = dateMatch.group(0)
	date2 = '    '
	ctry = 'tnu'
	illus = '    '
	audn = ' '
	form = 't'
	cont = 't   '
	gpub = ' '
	conf = '0'
	fest = '0'
	index = '0'
	pos_32 = ' '
	litF = '0'
	biog = ' '
	lng = 'eng'
	mrec = ' '
	cat_src = 'd'
	rec_008 = Field(tag='008', data = entered + dtst + dateStrip + date2 + ctry + illus + audn + form + cont + gpub + conf + fest + index + pos_32 + litF + biog + lng + mrec + cat_src)
	new_marc_rec.add_ordered_field(rec_008)

#----------------------------------------
	if not record['091']:
		reportNumber = record['088']['a']
		numberMatch = re.split('\W+', reportNumber) #regex to remove all punctuation from report number, returns a list
		new091 = ''.join(numberMatch)               #joins list together into normalized alphanumeric report identifier
		rec_091 = Field(tag='091', indicators=[' ', ' '], subfields=['a', str(new091)])
		new_marc_rec.add_ordered_field(rec_091)
	else:
		reportNumber = record['091']['a']
		rec_091 = Field(tag='091', indicators=[' ',' '], subfields=['a', str(reportNumber)])
		new_marc_rec.add_ordered_field(rec_091)

#----------------------------------------
	reportNumber2 = record['088']['a']
	rec_088 = Field(tag='088', indicators=[' ', ' '], subfields=['a', str(reportNumber2)])
	new_marc_rec.add_ordered_field(rec_088)

	
	print new_marc_rec
	marc_recs_out.write(new_marc_rec.as_marc())
	
marc_recs_out.close()
reader.close()


