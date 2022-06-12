import urllib
import json
import folium
import sys
import time

def finn_station_status_by_id(id, stations):
    for station in stations:
        if (station['station_id'] == str(id)):
            return station


def fetch_data(url):
    request = urllib.request.Request(url)
    request.add_header("Client-Identifier", "Pias Kart-Bysykkelkart")

    response = urllib.request.urlopen(request)
    read = json.loads(response.read())
    return read


def fetch_data_from_all_urls_in_feed(gbfs):
    feeds = gbfs['data']['nb']['feeds']
    infos = {}
    for obj in feeds:
        infos[obj['name']] = obj['url']

    for obj in feeds:
        infos[obj['name']] = fetch_data(obj['url'])

    return infos


def convert_and_format_time(time_in_seconds):
    local_time = time.localtime(time_in_seconds)
    return time.strftime('%d.%m.%Y %H:%M:%S', local_time)


def make_html_for_popup(station, station_status):
    title = station['name']
    num_bikes_available = str(station_status['num_bikes_available'])
    num_docks_available = str(station_status['num_docks_available'])
    address = str(station['address'])
    return """<html>
	<body>
	<h3>{title}</h3>
	<p>Tilgjengelige sykler: {num_bikes_available}</p>
	<p>Tilgjengelige låser: {num_docks_available}</p>
	<p>Adresse: {address}</p>
	</body>
	</html>
	""".format(**locals())


def format_output(station_status, station):
    spaces = '    '
    return ('Stasjon: ' + station['name'] + '\n'
          + spaces + 'Tilgjengelige sykler: ' + str(station_status['num_bikes_available']) + '\n'
          + spaces + 'Tilgjengelige låser:  ' + str(station_status['num_docks_available']) + '\n'
          + spaces + 'Adresse:              ' + str(station['address']) + '\n')

def add_station_marker_on_map(norge, station, station_status):
    norge.add_child(folium.Marker(
        location=[str(station['lat']), str(station['lon'])],
        tooltip=station['name'],
        popup=make_html_for_popup(station, station_status)))

def main():
    while 1:
        gbfs_url = "https://gbfs.urbansharing.com/oslobysykkel.no/gbfs.json"
        gbfs = fetch_data(gbfs_url)
        response_by_domain_name_map = fetch_data_from_all_urls_in_feed(gbfs)

        stations = response_by_domain_name_map['station_information']['data']['stations']
        stations.sort(key=lambda station: station['name'])

        last_updated_time = convert_and_format_time(gbfs['last_updated'])
        print('Sist oppdatert: ' + last_updated_time + '\n')

        norge = folium.Map(location=[59.930000, 10.743746], zoom_start=12.5, control_scale=True)

        with open("bysykkelstasjonsstatus.txt","w") as output_file:
            output_file.write('Sist oppdatert: ' + last_updated_time + '\n\n')
            for station in stations:
                station_status = finn_station_status_by_id(station['station_id'], response_by_domain_name_map['station_status']['data']['stations'])

                output = format_output(station_status, station)
                print(output)
                output_file.write(output + '\n')
                add_station_marker_on_map(norge, station, station_status)

        title_html = '''
            <h3 style="font-size:16px"><b>Sist oppdatert: {}</b></h3>
            '''.format(last_updated_time)

        norge.get_root().html.add_child(folium.Element(title_html))

        norge.save("kart.html")

        #Oppdater listen hvert minutt
        time.sleep(60)

if __name__ == "__main__":
    sys.exit(main())
