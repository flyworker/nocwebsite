$(document).ready(function(){
 var map = new GMaps({
    el: '#nodes_map',
    lat: 40.0,
    lng: -10.0,
    zoom: 3,
    zoomControl : true,
    panControl : false,
    mapTypeControl : false,
    streetViewControl : false,
    disableDoubleClickZoom: true,
  });

{% for node in nodes %}
    map.addMarker({
      lat: {{ node.geolat }},
      lng: {{ node.geolng }},
      title: '{{ node.locationdisplay }}',
      icon: 'http://maps.google.com/mapfiles/ms/icons/{% if node.state == "live" %}green{% endif %}{% if node.state == "inprogress" %}blue{% endif %}-dot.png',
      infoWindow: {
        content: '<p><img src="static/images/flags/{{ node.flag }}.gif"> {{ node.locationdisplay }}<br/><small>{% if node.state == "live" %}<b>Live</b> {{ node.livedisplay }}{% endif %}{% if node.state == "inprogress" %}<b>In Progress</b>{% endif %}</small><br/><small>{% if node.v4display %}IPv4{% endif %}   {% if node.v6display %}IPv6{% endif %}</small></p>'
      }
    });
{% endfor %}
});
