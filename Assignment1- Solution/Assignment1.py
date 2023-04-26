import csv

csv_file = open('Cards.csv', 'r') 
reader = csv.reader(csv_file, delimiter=';')
devices = {}
next(reader)
total_cards = 0
max_card_temp = 0
hottest_device = ''

for device, card, temp in reader:
    temp = int(temp)
    if device not in devices:
        devices[device] = {'total_of_cards': 1, 'high_temp_cards': 0, 'max_temp': temp, 'total_temp': [temp], 'hottest_card_name': card}
    else:
        devices[device]['total_of_cards'] += 1
        if temp > 70:
            devices[device]['high_temp_cards'] += 1
            devices[device]['hottest_card_name'] = card  
        if temp > devices[device]['max_temp']:
            devices[device]['max_temp'] = temp           
        devices[device]['total_temp'].append(temp)

for device, dt in devices.items():
    total_cards += dt['total_of_cards']
    avg_temp = sum(dt['total_temp'])/len(dt['total_temp'])
    devices[device]['avg_temp'] = int(avg_temp)
    if dt['max_temp'] > max_card_temp:
        max_card_temp = dt['max_temp']
        hottest_device = device

total_devices = len(devices)
hottest_card = devices[hottest_device]['hottest_card_name']  

html_file = open('report1.html', 'w')
html_file.write('<html>\n')
html_file.write('<head>\n')
html_file.write('<style>\n')
html_file.write('table, th, td {\n')
html_file.write('  border: 1px solid black;\n')
html_file.write('}\n')
html_file.write('</style>\n')
html_file.write('</head>\n')
html_file.write('<body>\n')
html_file.write('<h1>Summary</h1>\n')
html_file.write('<table>\n')
html_file.write(f'<tr><th>Total Devices</th><td>{total_devices}</td></tr>\n')
html_file.write(f'<tr><th>Total Cards</th><td>{total_cards}</td></tr>\n')
html_file.write(f'<tr><th>Max Card Temperature</th><td>{max_card_temp}</td></tr>\n')
html_file.write(f'<tr><th>Hottest Card / Device</th><td>{hottest_card} / {hottest_device}</td></tr>\n')
html_file.write('</table>\n')
html_file.write('</table>\n')
html_file.write('<h2>Devices</h2>\n')
html_file.write('<table>\n')
html_file.write('<tr><th>Device</th><th>Total # of Cards</th><th>High Temp. Cards #</th><th>Max. Temperature</th><th>Avg. Temperature</th></tr>\n')
for device, dt in devices.items():
    total_of_cards = dt['total_of_cards']
    high_temp_cards = dt['high_temp_cards']
    max_temp = dt['max_temp']
    avg_temp = dt['avg_temp']
    html_file.write(f'<tr><td>{device}</td><td>{total_of_cards}</td><td>{high_temp_cards}</td><td>{max_temp}</td><td>{avg_temp}</td></tr>\n')
html_file.write('</table>\n')
html_file.write('<h4>(High Temperature >= 70)</h4>\n')
html_file.write('</body>\n')
html_file.write('</html>\n')

csv_file.close()
html_file.close()

print(devices)