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
                  'Symbol':3,
                  'Package':4,
                  'Library':5}

import sys,csv
from urllib import urlopen
from sgmllib import SGMLParser

CSV_file_path = '.\parts_list.csv'
Incoming_list_path = '..\Incoming\incoming.txt'

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
            incoming_parts_contents = incoming_parts_contents + str(row)
            continue
        
        if row[Argument_list['Markup']] == 'GEN':
            continue
            #part = []

        elif row[Argument_list['Markup']] == 'DK':
            # print row
            try:
                dk_pn = row[Argument_list['DKey_Part']]
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
        
        for cell in headers:
           
            if cell == 'Name':
                CSV_header = CSV_header + ',Name'
                CSV_row = CSV_row + ','+row[Argument_list['Name']]
                
            elif cell == 'PPP':
                CSV_header = CSV_header+',PPP'
                CSV_row = CSV_row + ',1'
                
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
            
        #Open CSV parts file
        #loop through file until you find the correct library (or end)
        #then loop through and see if you find the same header
        #then append proper information at proper place

        CSV_file = open(CSV_file_path,'r')

        library_found = False
        part_inserted = False
        CSV_parts_lib = ''
        last_row = ''
        for CSV_library_row in CSV_file:
            if CSV_library_row == last_row and last_row != '\n':
                print "Ignoring repeated row " 
                continue
            if part_inserted == True:
                CSV_parts_lib = CSV_parts_lib + CSV_library_row
            elif row[Argument_list['DKey_Part']]+',' in CSV_library_row:
                if library_found:
                    print "Found part " + row[Argument_list['DKey_Part']]+ " in correct library " + row[Argument_list['Library']]+ ", replacing row"
                    if last_row != CSV_header + "\n":
                        #This prevents us from inserting the same header twice
                        CSV_parts_lib = CSV_parts_lib + CSV_header +"\n"
                        
                    CSV_parts_lib = CSV_parts_lib + CSV_row + "\n"
                    part_inserted = True
                else:
                    print "Found part " + row[Argument_list['DKey_Part']]+ " in incorrect library, removing row"
                    #the old header will remain, sadly
                    continue
            elif CSV_library_row == 'end\n':
                try:
                    
                    if library_found:
                        print "Found end of file in desired library " + row[Argument_list['Library']]
                        print "Inserting header and part " + row[Argument_list['DKey_Part']] + " rows"
                        #insert header and part then original row
                    else:
                        print CSV_library_row
                        print "Found end of file but not desired library " + row[Argument_list['Library']]
                        print "Inserting library " + row[Argument_list['Library']]+", header and part" + row[Argument_list['DKey_Part']] +" rows"
                        CSV_parts_lib = CSV_parts_lib + "library," + row[Argument_list['Library']] + "\n"
                    #insert library row
                    #insert header row
                    #insert part row
                        
                    CSV_parts_lib = CSV_parts_lib + CSV_header + "\n"
                    CSV_parts_lib = CSV_parts_lib + CSV_row + "\n"
                    CSV_parts_lib = CSV_parts_lib + CSV_library_row
                    part_inserted = True
                except IndexError,msg:
                    continue
                
            elif 'library,' in CSV_library_row:
                try:
                    if library_found:
                        print "Found end of desired library " + row[Argument_list['Library']] +" but no matching header"
                        print "Inserting header and part " + row[Argument_list['DKey_Part']] + " rows"
                        CSV_parts_lib = CSV_parts_lib + CSV_header + "\n"
                        CSV_parts_lib = CSV_parts_lib + CSV_row + "\n"
                        part_inserted = True
                        library_found = False
                        #insert header and part because we haven't found the right header
                        #then append
                    elif row[Argument_list['Library']]+'\n' in CSV_library_row:
                        print "Found desired library " + row[Argument_list['Library']]
                        library_found = True
                except IndexError,msg:
                    continue
                    
                CSV_parts_lib = CSV_parts_lib + CSV_library_row
            elif CSV_library_row == CSV_header and library_found:
                try:
                    
                    print "Found desired library " + row[Argument_list['Library']]+ " and matching header"
                    print "Inserting pre-existing header then new part " + + row[Argument_list['DKey_Part']] + " row"
                    CSV_parts_lib = CSV_parts_lib + CSV_library_row
                    CSV_parts_lib = CSV_parts_lib + CSV_row + "\n"
                    part_inserted = True               
                    #Append current row (it's the header)
                    #append part
                    #continue and append the rest of the rows
                except IndexError,msg:
                    print "Invalid row in incoming file: " + row
                    continue
            else:
                #append current row as we haven't found anything yet
                CSV_parts_lib = CSV_parts_lib + CSV_library_row

            last_row = CSV_library_row
            
        CSV_file.close()
        #print CSV_parts_lib
        try:
            CSV_file = open(CSV_file_path,'w')
        except Exception,msg:
            raise
        
        CSV_file.write(CSV_parts_lib)
        print "Rewrote CSV parts list file!\n"
        CSV_file.close()

    print incoming_parts_contents
if __name__=="__main__":
    try:
        main(sys.argv[1:])
    except SystemExit:
        print "A fatal error ocurred"


