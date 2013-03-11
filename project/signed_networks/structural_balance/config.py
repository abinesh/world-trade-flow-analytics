JSON_OUT_DIR = 'out/json'
HTML_OUT_DIR = 'out/html'

def output_file(year):
    return JSON_OUT_DIR + "/%s.json" % year


def output_file_html(year):
    return HTML_OUT_DIR + "/%s.html" % year


def html_header():
    return '''
    <!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8">
    <title>Mobile Patent Suits</title>
    <script type="text/javascript" src="file:///Users/abinesh/USC/isi/world-trade-flow-analytics/project/signed_networks/structural_balance/d3/js/d3.v2.js"></script>
    <script type="text/javascript" src="js/d3.v2.js"></script>
    <style type="text/css">

        path.link {
            fill: none;
            stroke: #0e6611;
            stroke-width: 0.3px;
        }

        path.link.negative {
            stroke: #66181f;
            stroke-width: 0.1px;
        }

        path.link.missing {
            display:none;
            /*stroke: #66181f;*/
            /*stroke-width: 0.1px;*/
        }

        circle {
            fill: #ccc;
            stroke: #333;
            stroke-width: 1.5px;
        }

        text {
            font: 10px sans-serif;
            pointer-events: none;
        }

        text.shadow {
            stroke: #fff;
            stroke-width: 3px;
            stroke-opacity: .8;
        }

    </style>
</head>
<body>
Modified from http://bl.ocks.org/1153292
<script type="text/javascript">

var links = [
    '''


def html_footer(year):
    return'''

];


var clusterNumberFor=function (country){
    return 1;
};

//version to push groups apart
/*
var year =  %s;
 var total_groups = 10;
var clusterNumbers ={
    "1969": {"Indonesia":6,
 "Falkland Is":10,
 "Guatemala":4,
 "Nepal":7,
 "Australia":6,
 "Finland":7,
 "St.Kt-Nev-An":1,
 "Angola":8,
 "Italy":2,
 "Haiti":4,
 "Taiwan":4,
 "Asia NES":6,
 "China HK SAR":6,
 "Paraguay":4,
 "South Africa":3,
 "Mongolia":4,
 "Fm Yemen Dm":3,
 "Seychelles":3,
 "Switz.Liecht":2,
 "Guadeloupe":5,
 "St.Helena":10,
 "New Zealand":6,
 "Turkmenistan":10,
 "Jordan":2,
 "Congo":7,
 "Fr.Guiana":4,
 "Kyrgyzstan":10,
 "Honduras":4,
 "Austria":2,
 "TFYR Macedna":10,
 "Chad":5,
 "Viet Nam":6,
 "Bolivia":3,
 "Bosnia Herzg":10,
 "Poland":2,
 "Gibraltar":3,
 "China SC":10,
 "Croatia":10,
 "Kazakhstan":10,
 "Korea D P Rp":6,
 "Venezuela":1,
 "Iran":1,
 "Portugal":8,
 "Mozambique":8,
 "Tajikistan":10,
 "Nicaragua":4,
 "Trinidad Tbg":4,
 "Occ.Pal.Terr":10,
 "Norway":9,
 "Pakistan":7,
 "USA":4,
 "Fm Yemen AR":6,
 "Niger":5,
 "Areas NES":2,
 "Iraq":2,
 "Czechoslovak":2,
 "Cambodia":6,
 "Czech Rep":10,
 "Myanmar":7,
 "Uzbekistan":10,
 "Kenya":3,
 "Bulgaria":2,
 "Greece":2,
 "EEC NES":10,
 "Nigeria":3,
 "Hungary":2,
 "Uruguay":2,
 "Gambia":3,
 "Br.Antr.Terr":10,
 "Fm Yugoslav":2,
 "Russian Fed":10,
 "Suriname":4,
 "Togo":5,
 "Kiribati":6,
 "Mauritania":2,
 "E Europe NES":10,
 "Brazil":4,
 "Armenia":10,
 "Japan":6,
 "Malaysia":6,
 "Guyana":4,
 "Ukraine":10,
 "Sweden":9,
 "Gabon":5,
 "Algeria":5,
 "Estonia":10,
 "China FTZ":10,
 "Oman":5,
 "Romania":2,
 "Mali":5,
 "Lithuania":10,
 "Lao P.Dem.R":6,
 "Argentina":4,
 "Madagascar":5,
 "New Calednia":6,
 "Singapore":6,
 "Cote Divoire":5,
 "Barbados":3,
 "Thailand":6,
 "Neth.Ant.Aru":4,
 "Malta":3,
 "El Salvador":4,
 "Cyprus":3,
 "Dem.Rp.Congo":2,
 "Bahrain":9,
 "Jamaica":4,
 "Cuba":6,
 "Malawi":3,
 "Syria":2,
 "Eur. EFTA NS":10,
 "Afr.Other NS":10,
 "Burundi":4,
 "Samoa":6,
 "Neutral Zone":10,
 "Zimbabwe":3,
 "Cent.Afr.Rep":5,
 "Mexico":4,
 "Canada":4,
 "Netherlands":2,
 "Asia West NS":10,
 "Georgia":10,
 "Chile":2,
 "Bahamas":4,
 "Kuwait":6,
 "Qatar":6,
 "Ghana":5,
 "China MC SAR":1,
 "Peru":1,
 "St.Pierre Mq":4,
 "Untd Arab Em":1,
 "Yugoslavia":10,
 "Libya":2,
 "Bermuda":3,
 "India":7,
 "Latvia":10,
 "Denmark":9,
 "Sierra Leone":3,
 "France,Monac":5,
 "LAIA NES":10,
 "Djibouti":2,
 "Papua N.Guin":6,
 "Liberia":2,
 "Philippines":6,
 "Israel":4,
 "Greenland":1,
 "Korea Rep.":4,
 "Rep Moldova":10,
 "Zambia":3,
 "Senegal":5,
 "Fm German DR":2,
 "Eq.Guinea":2,
 "Iceland":4,
 "Tunisia":5,
 "Fr Ind O":5,
 "CACM NES":10,
 "Belarus":10,
 "Benin":5,
 "Tanzania":3,
 "Azerbaijan":10,
 "Cameroon":5,
 "Spain":2,
 "Bangladesh":10,
 "Morocco":5,
 "Africa N.NES":10,
 "Ecuador":4,
 "Turkey":2,
 "Ethiopia":4,
 "Carib. NES":10,
 "Ireland":3,
 "Lebanon":2,
 "Int Org":10,
 "Eur.Other NE":10,
 "Dominican Rp":4,
 "Uganda":3,
 "Fiji":3,
 "Costa Rica":4,
 "Saudi Arabia":2,
 "Oth.Oceania":10,
 "Germany":10,
 "Sudan":1,
 "UK":3,
 "Albania":2,
 "Colombia":1,
 "Guinea":9,
 "GuineaBissau":8,
 "Slovenia":10,
 "Afghanistan":7,
 "Belize":1,
 "Slovakia":10,
 "Somalia":2,
 "Yemen":10,
 "Fm USSR":7,
 "US NES":6,
 "Burkina Faso":5,
 "Egypt":7,
 "Fm German FR":2,
 "Mauritius":3,
 "Rwanda":2,
 "China":6,
 "Sri Lanka":3,
 "Panama":4,
 "Belgium-Lux":2,
 },
    "1999": {"Indonesia":7,
 "Falkland Is":8,
 "Guatemala":3,
 "Nepal":5,
 "Australia":6,
 "Finland":7,
 "St.Kt-Nev-An":1,
 "Angola":3,
 "Italy":2,
 "Haiti":3,
 "Taiwan":9,
 "Asia NES":5,
 "China HK SAR":5,
 "Paraguay":4,
 "South Africa":1,
 "Mongolia":5,
 "Fm Yemen Dm":10,
 "Seychelles":1,
 "Switz.Liecht":1,
 "Guadeloupe":3,
 "St.Helena":5,
 "New Zealand":6,
 "Turkmenistan":2,
 "Jordan":5,
 "Congo":3,
 "Fr.Guiana":3,
 "Kyrgyzstan":2,
 "Honduras":3,
 "Austria":2,
 "TFYR Macedna":2,
 "Chad":8,
 "Viet Nam":5,
 "Bolivia":3,
 "Bosnia Herzg":2,
 "Poland":2,
 "Gibraltar":1,
 "China SC":10,
 "Croatia":2,
 "Kazakhstan":2,
 "Korea D P Rp":5,
 "Venezuela":3,
 "Iran":7,
 "Portugal":8,
 "Mozambique":8,
 "Tajikistan":2,
 "Nicaragua":3,
 "Trinidad Tbg":3,
 "Occ.Pal.Terr":10,
 "Norway":1,
 "Pakistan":7,
 "USA":3,
 "Fm Yemen AR":10,
 "Niger":8,
 "Areas NES":7,
 "Iraq":3,
 "Czechoslovak":10,
 "Cambodia":3,
 "Czech Rep":2,
 "Myanmar":5,
 "Uzbekistan":2,
 "Kenya":1,
 "Bulgaria":2,
 "Greece":2,
 "EEC NES":7,
 "Nigeria":3,
 "Hungary":2,
 "Uruguay":4,
 "Gambia":9,
 "Br.Antr.Terr":5,
 "Fm Yugoslav":10,
 "Russian Fed":2,
 "Suriname":1,
 "Togo":9,
 "Kiribati":5,
 "Mauritania":8,
 "E Europe NES":7,
 "Brazil":4,
 "Armenia":9,
 "Japan":5,
 "Malaysia":5,
 "Guyana":3,
 "Ukraine":2,
 "Sweden":1,
 "Gabon":3,
 "Algeria":8,
 "Estonia":1,
 "China FTZ":5,
 "Oman":5,
 "Romania":2,
 "Mali":5,
 "Lithuania":2,
 "Lao P.Dem.R":5,
 "Argentina":4,
 "Madagascar":8,
 "New Calednia":5,
 "Singapore":5,
 "Cote Divoire":8,
 "Barbados":1,
 "Thailand":5,
 "Neth.Ant.Aru":3,
 "Malta":8,
 "El Salvador":3,
 "Cyprus":1,
 "Dem.Rp.Congo":9,
 "Bahrain":5,
 "Jamaica":3,
 "Cuba":2,
 "Malawi":1,
 "Syria":2,
 "Eur. EFTA NS":10,
 "Afr.Other NS":7,
 "Burundi":2,
 "Samoa":6,
 "Neutral Zone":5,
 "Zimbabwe":1,
 "Cent.Afr.Rep":9,
 "Mexico":3,
 "Canada":3,
 "Netherlands":1,
 "Asia West NS":7,
 "Georgia":2,
 "Chile":5,
 "Bahamas":1,
 "Kuwait":7,
 "Qatar":5,
 "Ghana":1,
 "China MC SAR":3,
 "Peru":3,
 "St.Pierre Mq":3,
 "Untd Arab Em":5,
 "Yugoslavia":2,
 "Libya":2,
 "Bermuda":1,
 "India":5,
 "Latvia":1,
 "Denmark":1,
 "Sierra Leone":9,
 "France,Monac":8,
 "LAIA NES":7,
 "Djibouti":3,
 "Papua N.Guin":6,
 "Liberia":9,
 "Philippines":3,
 "Israel":3,
 "Greenland":1,
 "Korea Rep.":5,
 "Rep Moldova":2,
 "Zambia":5,
 "Senegal":8,
 "Fm German DR":10,
 "Eq.Guinea":8,
 "Iceland":1,
 "Tunisia":8,
 "Fr Ind O":8,
 "CACM NES":10,
 "Belarus":2,
 "Benin":4,
 "Tanzania":5,
 "Azerbaijan":2,
 "Cameroon":8,
 "Spain":8,
 "Bangladesh":3,
 "Morocco":8,
 "Africa N.NES":7,
 "Ecuador":3,
 "Turkey":2,
 "Ethiopia":2,
 "Carib. NES":10,
 "Ireland":1,
 "Lebanon":1,
 "Int Org":10,
 "Eur.Other NE":7,
 "Dominican Rp":3,
 "Uganda":8,
 "Fiji":6,
 "Costa Rica":3,
 "Saudi Arabia":5,
 "Oth.Oceania":5,
 "Germany":2,
 "Sudan":5,
 "UK":1,
 "Albania":2,
 "Colombia":3,
 "Guinea":9,
 "GuineaBissau":5,
 "Slovenia":2,
 "Afghanistan":7,
 "Belize":1,
 "Slovakia":2,
 "Somalia":5,
 "Yemen":5,
 "Fm USSR":10,
 "US NES":5,
 "Burkina Faso":8,
 "Egypt":2,
 "Fm German FR":10,
 "Mauritius":1,
 "Rwanda":9,
 "China":5,
 "Sri Lanka":3,
 "Panama":3,
 "Belgium-Lux":9,
 },
};
var clusterNumberFor=function(country){
 if (year in clusterNumbers && country in clusterNumbers[year])
 return clusterNumbers[year][country];
 else return 20;
};
*/

var nodes = {};

// Compute the distinct nodes from the links.
links.forEach(function (link) {
    link.source = nodes[link.source] || (nodes[link.source] = {name:link.source,group:clusterNumberFor(link.source)});
    link.target = nodes[link.target] || (nodes[link.target] = {name:link.target,group:clusterNumberFor(link.target)});
});

var w = 1000,
        h = 1000;

var force = d3.layout.force()
        .nodes(d3.values(nodes))
        .links(links)
        .size([w, h])
        .linkDistance(function (n) {
            if (n.type == "negative") return 500;
            else return 250;
         })
        .charge(-30)
        .gravity(0.1)
        .on("tick", tick)
        .start();

var svg = d3.select("body").append("svg:svg")
        .attr("width", w)
        .attr("height", h);

// Per-type markers, as they don't inherit styles.
svg.append("svg:defs").selectAll("marker")
        .data(["positive", "licensing", "negative"])
        .enter().append("svg:marker")
        .attr("id", String)
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 15)
        .attr("refY", -1.5)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto");

var path = svg.append("svg:g").selectAll("path")
        .data(force.links())
        .enter().append("svg:path")
        .attr("class", function (d) {
            return "link " + d.type;
        })
        .attr("marker-end", function (d) {
            return "url(#" + d.type + ")";
        });

var colorScale = d3.scale.category20();

var circle = svg.append("svg:g").selectAll("circle")
        .data(force.nodes())
        .enter().append("svg:circle")
        .attr("r", 2.8)
        .style("fill", function(d) { return colorScale(d.group); })
        .call(force.drag);

var text = svg.append("svg:g").selectAll("g")
        .data(force.nodes())
        .enter().append("svg:g");

// A copy of the text with a thick white stroke for legibility.
text.append("svg:text")
        .attr("x", 8)
        .attr("y", ".31em")
        .attr("class", "shadow")
        .text(function (d) {
            return d.name;
        });

text.append("svg:text")
        .attr("x", 8)
        .attr("y", ".31em")
        .text(function (d) {
            return d.name;
        });

// Use elliptical arc path segments to doubly-encode directionality.
function tick() {
    path.attr("d", function (d) {
        var dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy)*10;
        return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
    });

    circle.attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
    });

    text.attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
    });
}

//version to push groups apart
/* var nb_group = total_groups;
 var angle = 2*Math.PI/nb_group;
 var intensity = 250;

function tick() {
    path.attr("d", function (d) {
        var sourcexm = d.source.x + intensity*Math.cos(angle* d.source.group);
        var sourceym = d.source.y + intensity*Math.sin(angle* d.source.group);
        var targetxm = d.target.x + intensity*Math.cos(angle* d.target.group);
        var targetym = d.target.y + intensity*Math.sin(angle* d.target.group);
        var dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy)*100;
        return "M" + sourcexm + "," + sourceym + "A" + dr + "," + dr + " 0 0,1 " + targetxm + "," + targetym;
    });

    circle.attr("transform", function (d) {
        var xm = d.x + intensity*Math.cos(angle*d.group);
        var ym = d.y + intensity*Math.sin(angle*d.group);
        return "translate(" + xm + "," + ym + ")";
    });

    text.attr("transform", function (d) {
        var xm = d.x + intensity*Math.cos(angle*d.group);
        var ym = d.y + intensity*Math.sin(angle*d.group);
        return "translate(" + xm + "," + ym + ")";
    });
}
*/

</script>
</body>
</html>''' % year
