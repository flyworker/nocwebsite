var map;
$(document).ready(function(){
 map = new GMaps({
    el: '#nodes_map',
    lat: 21.17,
    lng: 17.53,
    zoom: 2,
    zoomControl : true,
    panControl : false,
    mapTypeControl : false,
    streetViewControl : false,
    disableDoubleClickZoom: true,
    /* dragend: function(e) {
      console.log(e);
     } */
  });

{% for node in nodes %}
    map.addMarker({
      lat: {{ node.geolat }},
      lng: {{ node.geolng }},
      title: '{{ node.locationdisplay }}',
      icon: 'https://maps.google.com/mapfiles/ms/icons/{% if node.state == "maintenance" %}orange{% endif %}{% if node.state == "live" %}green{% endif %}{% if node.state == "inprogress" %}blue{% endif %}-dot.png',
      infoWindow: {
        content: '<p><img src="static/images/flags/{{ node.flag }}.gif"> {{ node.locationdisplay }}<br/><small>{% if node.state == "live" %}<b>Live</b> {{ node.livedisplay }}{% endif %}{% if node.state == "inprogress" %}<b>In Progress</b>{% endif %}{% if node.state == "maintenance" %}<b>Under maintenance</b>{% endif %}</small><br/><small>{% if node.v4display %}IPv4{% endif %}   {% if node.v6display %}IPv6{% endif %}</small></p>'
      }
    });
{% endfor %}
});
