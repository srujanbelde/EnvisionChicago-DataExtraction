import csv

with open(('restaurants_60601-60606.csv'), 'r', encoding='UTF8') as csv_file:
    csv_reader=csv.reader(csv_file)
    with open(('B_restaurants.csv'), 'w', newline='',encoding='UTF8') as csv_output:
        csv_writter=csv.writer(csv_output,delimiter=',')
        count = 0
        for line in csv_reader:
            if count ==0:
                csv_writter.writerow(line)
            name=line[1]
            firstletter=name[0]
            if firstletter == "B":
                csv_writter.writerow(line)
            if firstletter == "b":
                csv_writter.writerow(line)
            count=count+1