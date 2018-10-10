import textract
base = '/Users/bhashi/Desktop/ES_Daily_Data'
no_of_strategies = input('No of Strategies: ')
for strategy_number in range(1, int(no_of_strategies)+1):
    file = textract.process(base+'/'+str(strategy_number)+'/Strategy Code.doc')
    str_file = file.decode("ascii")
    text_file = open(base+'/'+str(strategy_number)+'/Strategy Code.txt', 'w')
    text_file.write(str_file)
    text_file.close()
