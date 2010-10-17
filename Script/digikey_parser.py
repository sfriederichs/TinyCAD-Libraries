#This script is to be called from the command line thusly:
#python digikey_parser <DIGIKEY PART #> <PART NAME> <SYMBOL> <PACKAGE> <LIBRARY>
#<PART NAME> is what should show up in the library under 'Name'
#<LIBRARY> is which library the part should be placed in
#Thus, if I wanted to place a nice 1206 red LED into the library I'd say:

#python digikey_parser.py L62011CT-ND LED_RED_1206 LED LED_1206 sm_Semiconductor

#if the library doesn't exist, it will make it
#eventually, the above will be read from a text file which will then be wiped after it is used

#Parts per package is always assumed to be 1 unless I can find something in Digikey to clue me
#into this value

#But in general, one chip is always one symbol in my scheme, and there's only one part (chip) per chip (chip)

#TODO:
#This script won't alert you when there's an invalid row in the incoming text file

#Generalize this: make it so that it doesn't have to be a digikey part
#The file might look something like:
#DK L62011CT LED_RED_1206 LED LED_1206 sm_Semiconductor
#GEN PICAXE_18M PICAXE_18M DIP18_300 gen_uC_Picaxe

#Create a new Python script to read in new symbol files and put them in symbols.TCLib

#Figure out how to re-upload the CSV file to Google Docs once it's updated

Argument_list = { 'Markup':0,
                  'DKey_Part':1,
                  'Name':2,
                  'Ref':3,
                  'Symbol':4,
                  'Package':5,
                  'Library':6}

import sys,csv
from urllib import urlopen
from sgmllib import SGMLParser

CSV_parts_file_path = '.\Libraries\CSV\parts_list.csv'
Incoming_list_path = '.\Incoming\incoming.txt'

#This is the data read from the web page
#headers = ['Digi-Key Part Number',
#           'Manufacturer',
#           'Manufacturer Part Number',
#           'Description',
#           'Price Break',
#           'Unit Price',
#           'Extended Price',
#           'First Name',
#           'Voltage - Rated',
#           'Frequency',
#           'Voltage - Forward (Vf) Typ',
#           'Color',
#           'Package / Case']

#This is the data read from the web page and also
#the order in which the data should be put into the row
#If a piece of data isn't in the data retrieved from Digikey then it is ignored
#thus you if you have a capacitor, only capacitance is found
#if you have a resistor, only resistance is found, etc
required_headers = { 'Markup':0,
                     'Name':1,
                     'PPP':2,
                     'Ref':3,
                     'Symbol':4,
                     'Package':5,
                     'Description':6}
headers = ['Markup',
              'Name',
              'PPP',
              'Ref',
              'Symbol',
              'Package',
              'Description',
              'Blank',
              'Color',
              'Resistance In Ohms',
              'Capacitance',
              'Inductance',
              'Frequency',
              'Frequency Tolerance',
              'Load Capacitance',
              'Value',
              'Tolerance',
              'Number of Positions',
              'Number of Rows',
              'Row Spacing',
              'Pitch',
              'Contact Type',
              'Voltage - Forward (Vf) Typ',
              'Voltage - Supply',
              'Current',
              'Voltage - Rated',
              'Voltage Range',
              'Current Rating',
              'DC Resistance (DCR)',   
              'Operating Temperature',
              'Type',
              'Interface',
              'Pin or Socket',
              'Contact Termination',
              'Wire Gauge',
              'Contact Finish',
              'Color',
              'Size / Dimension',
              'Manufacturer',
              'Manufacturer Part Number',
              'Digi-Key Part Number',
              'Price Break',
              'Extended Price']

#This is a substitution list for some of the more vague Digikey terms
#if a term has no substitution then the original header value from Digikey is used

CSV_substitutions = { 'Price Break':'Min Quantity',
                       'Extended Price':'Price per min',
                       'Voltage - Forward (Vf) Typ':'Forward Voltage'}


                  
                  
class DK_Parser(SGMLParser):
    def reset(self):

        SGMLParser.reset(self)

        self.last_td = ''
        self.inside_th = False
        self.inside_td = False
        self.grab_data = False
        self.part_info = {}
        self.hdr_index = 0
        self.row_hdrs = []

    def start_tr(self, attrs): # row
        self.first_header_in_row = True

    def start_th(self, attrs): # header cell
        if self.first_header_in_row:
            self.first_header_in_row = False
            self.row_hdrs = []
            self.hdr_index = 0
        self.inside_th = True

    def end_th(self):
        self.inside_th = False

    def start_td(self, attrs): # data cell
        self.inside_td = True

    def end_td(self): 
        self.inside_td = False
        self.hdr_index = self.hdr_index+1

    def handle_data(self,text):
        text = text.strip()
        if self.inside_th:
            if text in headers:
                self.row_hdrs.append(text)
                self.last_td = ''
                self.grab_data = True
            else:
                self.grab_data = False
        elif self.inside_td and self.grab_data:
            if self.hdr_index:
                self.last_td = ''
            if self.hdr_index < len(self.row_hdrs):
                self.last_td = self.last_td + text
                self.part_info[self.row_hdrs[self.hdr_index]] = self.last_td

def main(argv=None):
    incoming_parts = csv.reader(file(Incoming_list_path))
    


    
#    for k,v in parser.part_info.items():
#        print k,":",v.strip(",")




    incoming_parts_contents = ''
    for row in incoming_parts:

        try:
            if row[Argument_list['Library']] == 'just a test':
                break
        except IndexError,msg:
            print "Invalid row in incoming file: " + str(row)
            incoming_parts_contents = incoming_parts_contents + ','.join(row)
            continue
        
        if row[Argument_list['Markup']] == 'GEN':
            continue
            #part = []

        elif row[Argument_list['Markup']] == 'DK':
            # print row
            try:
                dk_pn = row[Argument_list['DKey_Part']]
                dk_pn.replace('+','%2B')
                print 'Part number is ' + dk_pn
            except IndexError,msg:
                continue
            
            dk_url = 'http://search.digikey.com/scripts/DkSearch/dksus.dll'
            dk_params = '?Detail&name='

            sock = urlopen(dk_url + dk_params + dk_pn)

            parser = DK_Parser()
            parser.feed(sock.read())
            sock.close()
            parser.close()
            
            part = parser.part_info.items()
            #print part
            
        CSV_row = 'part'
        CSV_header = 'header'
        CSV_library = 'library,' + row[Argument_list['Library']]
        for cell in headers:
           
            if cell == 'Name':
                CSV_header = CSV_header + ',Name'
                CSV_row = CSV_row + ','+row[Argument_list['Name']]
                
            elif cell == 'PPP':
                CSV_header = CSV_header+',PPP'
                CSV_row = CSV_row + ',1'

            elif cell == 'Ref':
                CSV_header = CSV_header + ',Ref'
                try:
                    CSV_row = CSV_row + ',' + row[Argument_list['Ref']]
                except IndexError,msg:
                    print "Error, no ref name supplied"
                    raise
            elif cell == 'Symbol':
                CSV_header = CSV_header + ',Symbol'
                try:
                    CSV_row = CSV_row + ',' + row[Argument_list['Symbol']]
                except IndexError,msg:
                    print "Error, no symbol name supplied"
                    raise
            elif cell == 'Package':
                try:
                    CSV_header = CSV_header + ',Package'
                    CSV_row = CSV_row + ',' + row[Argument_list['Package']]
                except IndexError,msg:
                    print "Error, no package supplied"
                    raise
            elif cell == 'Blank':
                CSV_header = CSV_header + ','
                CSV_row = CSV_row + ','
            else:
                for k,v in part:
                    if k == cell:
                        
                        try:
                            k = CSV_substitutions[k]
                        except Exception,msg:
                            pass
                        #For some reason strip doesn't work, but replace does
                        value = str(v)
                        CSV_row = CSV_row + ',' + value.replace(',','')
                        CSV_header = CSV_header + ',' + k 
                        break
            

        CSV_row += '\n'
        CSV_library += '\n'
        CSV_header += '\n'
        #print CSV_row
        
        #Open CSV parts file
        #loop through file until you find the correct library (or end)
        #then loop through and see if you find the same header
        #then append proper information at proper place

        
                    
        CSV_parts_file = csv.reader(file(CSV_parts_file_path))
        library_found = False
        part_inserted = False
        header_inserted = False
        
        last_row = ''
        current_library = ''
        new_CSV_parts_lib = ''
        current_header = ''
        insert_part = False
        add_last_row = False
       
        
        for CSV_parts_library_row in CSV_parts_file:
            #Ignore blank rows
            #print ','.join(last_row)
            #print ','.join(CSV_parts_library_row)
            #print '\n'
            
            try:
                if CSV_parts_library_row[0] == '':
                    continue
            except IndexError,msg:
                continue

            try:
                if last_row[0] == '':
                    print 'Empty row'
            except IndexError,msg:
                last_row = CSV_parts_library_row
                continue
                #Preserve blank rows
                    
            if row[Argument_list['DKey_Part']] in CSV_parts_library_row:
                print 'Found duplicate part'
                continue

            if last_row[required_headers['Markup']] == 'library':
                
                if CSV_parts_library_row[required_headers['Markup']] == 'library' or CSV_parts_library_row[required_headers['Markup']] == 'end':
                    print 'Found unused library: ' + last_row[required_headers['Name']]
                    #last_row = CSV_parts_library_row
                    add_last_row = False
                else:
                    #write last row
                    if library_found and part_inserted == False:
                        print 'Inserting part at the end of current library'
                        insert_part = True
                        
                    add_last_row = True
                    current_library = last_row[required_headers['Name']]
                    #print '(1) Current library is ' + current_library
                   

            elif last_row[required_headers['Markup']] == 'header':
                #print CSV_parts_library_row
                if CSV_parts_library_row[required_headers['Markup']] == ('header' or 'library' or 'end'):
                    #print '(1) Unused header detected'
                    add_last_row = False
                elif CSV_parts_library_row[required_headers['Markup']] == 'library':
                    #print '(2) Unused header detected'
                    add_last_row = False
                elif CSV_parts_library_row[required_headers['Markup']] == 'end':
                    #print '(3) Unused header detected'
                    add_last_row = False
                else:
                    add_last_row = True

            elif last_row == CSV_parts_library_row:
                #print 'Found duplicate row'
                add_last_row = False
            else:
                add_last_row = True

            if current_library == row[Argument_list['Library']]:
                library_found = True
                
            if insert_part:
                print 'Inserting part'
                if header_inserted == False:
                    new_CSV_parts_lib += CSV_header
                    
                part_inserted = True

                insert_part = False
                new_CSV_parts_lib += CSV_row
                
            if add_last_row:
                new_CSV_parts_lib += ','.join(last_row)+'\n'
                add_last_row = False
                
            last_row = CSV_parts_library_row

        #Adding last_row

        #You might have to insert the part at the end
        if not part_inserted:
            if not library_found:
                new_CSV_parts_lib += 'library,'+row[Argument_list['Library']] + '\n'
            new_CSV_parts_lib += CSV_header
            new_CSV_parts_lib += CSV_row
        new_CSV_parts_lib += ','.join(last_row)
        
        #print new_CSV_parts_lib
        CSV_file = open(CSV_parts_file_path,'w')
        CSV_file.write(new_CSV_parts_lib)
        CSV_file.close()

        
        incoming_parts_file = open(Incoming_list_path,'w')
        incoming_parts_file.write(incoming_parts_contents)
        incoming_parts_file.close()
        
        #print '\n'
        #print CSV_header

    print incoming_parts_contents
    
if __name__=="__main__":
    try:
        main(sys.argv[1:])
    except SystemExit:
        print "A fatal error ocurred"


