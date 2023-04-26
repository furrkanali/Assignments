import csv

devices_csv = []
dt_dict = {}
pon_counts = {}
pon_utilization = {}
devices_dict = {}


def read_csv(file_path):
    csv_file = open(file_path, 'r')
    reader = csv.reader(csv_file, delimiter=',')
    next(reader)
    return csv_file,reader

def close_csv(csv_file):
    csv_file.close()

csv_file1, reader1  = read_csv('devices.csv')
for row in reader1:
    devices_csv.append(row[0])
    devices_dict[row[0]] = row[1]

csv_file2, reader2 = read_csv('pon_ports.csv')
for object_id, pon_type, active_ont_count, max_ont_capacity in reader2:
    server, board, pon = object_id.split(':')
    active_ont_count = int(active_ont_count)
    max_ont_capacity = int(max_ont_capacity)
    if server in dt_dict:
        if board in dt_dict[server]:
            dt_dict[server][board]['active_count'] += active_ont_count
            dt_dict[server][board]['max_capacity'] += max_ont_capacity
        else:
            dt_dict[server][board] = {'active_count': active_ont_count, 'max_capacity': max_ont_capacity}
    else:
        dt_dict[server] = {board: {'active_count': active_ont_count, 'max_capacity': max_ont_capacity}}
    if server not in devices_csv:
        continue
    if (server, pon_type) in pon_counts:
        pon_counts[(server, pon_type)] += 1 
    else:
        pon_counts[(server, pon_type)] = 1

for server in dt_dict:
    for board in dt_dict[server]:
        max_capacity = dt_dict[server][board]['max_capacity']
        active_count = dt_dict[server][board]['active_count']
        pon_utilization[(server, board)] = {'PON Utilization %': round(active_count/max_capacity*100, 2)}

sorted_pon_utilization = sorted(pon_utilization.items(), key=lambda x: x[1]['PON Utilization %'], reverse=True)
sorted_pon_counts = sorted(pon_counts.items(), key=lambda x: x[1], reverse=True)

html_file = open('report2.html', 'w')
html_file.write('<html>\n')
html_file.write('<head>\n')
html_file.write('<h2>Pon Report</h2>\n')
html_file.write('<style>\n')
html_file.write('table, th, td {\n')
html_file.write('  border: 1px solid black;\n')
html_file.write('}\n')
html_file.write('</style>\n')
html_file.write('</head>\n')
html_file.write('<body>\n')
html_file.write('<h3>Pon Utilization of LT Boards</h3>\n')
html_file.write('<table>\n')
html_file.write('<tr><th>Server Name</th><th>Board Name</th><th>PON Utilization %</th></tr>\n')
for item in sorted_pon_utilization:
    server, board = item[0]
    utilization = item[1]['PON Utilization %']
    html_file.write(f'<tr><td>{server}</td><td>{board}</td><td>{utilization}</td></tr>\n')
html_file.write('</table>\n')
html_file.write('<h3>Counts of Pon Types in Servers</h3>\n')
html_file.write('<table>\n')
html_file.write('<tr><th>Server Type</th><th>Server Name</th><th>PON Type</th><th>Pon Count</th></tr>\n')
for (server, pon_type), count in sorted_pon_counts:
    devices = devices_dict.get(server, 'N/A')
    html_file.write('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(devices, server, pon_type, count))
html_file.write('</table>\n')
html_file.write('</body>\n')
html_file.write('</html>\n')

close_csv(csv_file1)
close_csv(csv_file2)
html_file.close()