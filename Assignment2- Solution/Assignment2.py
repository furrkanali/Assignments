import csv

devices_csv = []
dt_dict = {}
pon_counts = {}
pon_utilization = {}
devices_dict = {}

csv_file1 = open('devices.csv', 'r') 
reader1 = csv.reader(csv_file1, delimiter=',')
next(reader1)

csv_file2 = open('pon_ports.csv', 'r') 
reader2 = csv.reader(csv_file2, delimiter=',')
next(reader2)

for row in reader1:
    devices_csv.append(row[0])
    devices_dict[row[0]] = row[1]

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

with open('pon_counts.html', 'w') as f:
    f.write('<html>\n')
    f.write('<head>\n')
    f.write('<title>PON Counts</title>\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('<h1>PON Counts</h1>\n')
    f.write('<table>\n')
    f.write('<tr><th>Server</th><th>PON Type</th><th>Count</th><th>Devices</th></tr>\n')
    for (server, pon_type), count in sorted_pon_counts:
        devices = devices_dict.get(server, 'N/A')
        f.write('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(server, pon_type, count, devices))
    f.write('</table>\n')
    f.write('</body>\n')
    f.write('</html>\n')

print('HTML file created:', os.path.abspath('pon_counts.html'))



# with open('output.html', 'w') as file:
#     # Write the HTML code
#     file.write('<html>\n')
#     file.write('<head>\n')
#     file.write('<title>PON Utilization Report</title>\n')
#     file.write('</head>\n')
#     file.write('<body>\n')

#     # Write the sorted_pon_utilization table
#     file.write('<h2>PON Utilization</h2>\n')
#     file.write('<table>\n')
#     file.write('<tr><th>Server</th><th>Board</th><th>PON Utilization %</th></tr>\n')
#     for item in sorted_pon_utilization:
#         server, board = item[0]
#         utilization = item[1]['PON Utilization %']
#         file.write(f'<tr><td>{server}</td><td>{board}</td><td>{utilization}</td></tr>\n')
#     file.write('</table>\n')
