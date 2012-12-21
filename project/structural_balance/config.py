JSON_OUT_DIR = 'out/json'
HTML_OUT_DIR = 'out/html'

def output_file(year):
    return JSON_OUT_DIR + "/%s.json" % year

def output_file_html(year):
    return HTML_OUT_DIR + "/%s.html" % year




html_header = '''
    <!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8">
    <title>Mobile Patent Suits</title>
    <script type="text/javascript" src="http://mbostock.github.com/d3/d3.js?1.29.1"></script>
    <script type="text/javascript" src="http://mbostock.github.com/d3/d3.geom.js?1.29.1"></script>
    <script type="text/javascript" src="http://mbostock.github.com/d3/d3.layout.js?1.29.1"></script>
    <style type="text/css">

        path.link {
            fill: none;
            stroke: #0e6611;
            stroke-width: 0.25px;
        }

        path.link.negative {
            stroke: #66181f;
            stroke-width: 0.1px;
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

html_footer = '''
    ];

var nodes = {};

// Compute the distinct nodes from the links.
links.forEach(function (link) {
    link.source = nodes[link.source] || (nodes[link.source] = {name:link.source});
    link.target = nodes[link.target] || (nodes[link.target] = {name:link.target});
});

var w = 1000,
        h = 1000;

var force = d3.layout.force()
        .nodes(d3.values(nodes))
        .links(links)
        .size([w, h])
        .linkDistance(function (n) {
            if (n.type == "negative") return 600;
            if (n.type == "missing") return 300;
            else return 10;
        })
        .charge(-300)
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

var circle = svg.append("svg:g").selectAll("circle")
        .data(force.nodes())
        .enter().append("svg:circle")
        .attr("r", 2)
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
                dr = Math.sqrt(dx * dx + dy * dy);
        return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
    });

    circle.attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
    });

    text.attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
    });
}

</script>
</body>
</html>
    '''
