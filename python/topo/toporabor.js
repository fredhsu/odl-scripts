var w = 400,
    h = 400,
    fill = d3.scale.category20();

var vis = d3.select("#chart")
.append("svg:svg")
.attr("width", w)
.attr("height", h);

d3.json("topo.json", function(json) {
  var topo = d3.layout.force()
  .charge(-120)
  .linkDistance(30)
  .nodes(json.nodes)
  .links(json.links)
  .size([w, h])
  .start();

var link = vis.selectAll("line.link")
  .data(json.links)
  .enter().append("svg:line")
  .attr("class", "link")
  .style("stroke-width", function(d) { return Math.sqrt(d.value); })
  .attr("x1", function(d) { return d.source.x; })
  .attr("y1", function(d) { return d.source.y; })
  .attr("x2", function(d) { return d.target.x; })
  .attr("y2", function(d) { return d.target.y; });

var node = vis.selectAll("circle.node")
  .data(json.nodes)
  .enter().append("svg:circle")
  .attr("class", "node")
  .attr("cx", function(d) { return d.x; })
  .attr("cy", function(d) { return d.y; })
  .attr("r", 5)
  .style("fill", function(d) { return fill(d.group); })
  .call(topo.drag);

node.append("svg:title")
  .text(function(d) { return d.name; });
var text = node.append("svg:circle").selectAll("circle.node")
  .attr("dx", 12)
  .attr("dy", ".35em")
  .text(function(d) { return d.id });

vis.style("opacity", 1e-6)
  .transition()
  .duration(1000)
  .style("opacity", 1);

topo.on("tick", function() {
  link.attr("x1", function(d) { return d.source.x; })
  .attr("y1", function(d) { return d.source.y; })
  .attr("x2", function(d) { return d.target.x; })
  .attr("y2", function(d) { return d.target.y; });

node.attr("cx", function(d) { return d.x; })
  .attr("cy", function(d) { return d.y; });
});
});
