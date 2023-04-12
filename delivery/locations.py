import folium
import geocoder

def userlocation(pos=[]):
	# print("My location is...",pos)
	lat, lng = pos[0], pos[1]
	map = folium.Map(location=[lat, lng], zoom_start=15)
	folium.Marker([lat, lng]).add_to(map)
	map = map._repr_html_()

	return map