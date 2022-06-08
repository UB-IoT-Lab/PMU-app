function dist_delay(data)
{
    // set the dimensions and margins of the graph
        var margin = { top: 10, right: 30, bottom: 50, left: 30 },
            width = 600 - margin.left - margin.right,
            height = 450 - margin.top - margin.bottom;

        // append the svg object to the body of the page
        var svg2 = d3.select("#my_dist")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");
        plotdist(data)
        // get the data
         function plotdist(data) {
            
            var x = d3.scaleLinear()
                 .domain(d3.extent(data)).nice()
                 .range([margin.left, width - margin.right])
            thresholds = x.ticks(100)
            bins = d3.histogram()
                 .domain(x.domain())
                 .thresholds(thresholds)
                 (data) 
            function kde(kernel, thresholds, data) {
                 return thresholds.map(t => [t, d3.mean(data, d => kernel(t - d))]);
             }

            function epanechnikov(bandwidth) {
                return x => Math.abs(x /= bandwidth) <= 1 ? 0.75 * (1 - x * x) / bandwidth : 0;
            }
            density = kde(epanechnikov(0.005), thresholds, data)
            
            function convertRange(value, r1, r2) {
                 return (value - r1[0]) * (r2[1] - r2[0]) / (r1[1] - r1[0]) + r2[0];
             }
            
            
            var maxRow = density.map(function (row) { return Math.max.apply(Math, row); });
            var max = Math.max.apply(null, maxRow);
            var sum = maxRow.reduce((partialSum, a) => partialSum + a, 0);
            var yax = (d3.max(bins, d => d.length) / data.length)
            var y = d3.scaleLinear()
                 .range([height, 0]);
                y.domain([0, d3.max(bins, function (d) { return d.length; })/data.length]);   // d3.hist has to be called before the Y axis obviously
                
            for (let i = 0; i < density.length; i++) {
                 density[i][1] = convertRange(density[i][1],[0,max],[0,max/sum])
             }
            var xAxis = d3.scaleLinear()
                 .domain([d3.extent(data)[0] * 1000, d3.extent(data)[1] * 1000]).nice()
                 .range([margin.left, width - margin.right])

            svg2.append("g")
                 .attr("transform", "translate(0," + height + ")")
                 .call(d3.axisBottom(xAxis));
            svg2.append("g")
                 .attr("transform", `translate(${margin.left},0)`)
                 .call(d3.axisLeft(y)
                    .ticks(null,"%"));
            
            
            svg2.append("g")
                 .attr("fill", "#bbb")
                .selectAll("rect")
                 .data(bins)
                 .enter()
                 .append("rect")
                 .attr("x", d => x(d.x0) + 1)
                .attr("y", d => y(d.length / data.length))
                 .attr("width", function (d) { return x(d.x1) - x(d.x0) - 1; })
                 .attr("height", function (d) { return height - y(d.length / data.length); })
                 .style("fill", "#0a74bf")
                 .attr("opacity", "1")

             svg2.append("path")
                 .datum(density)
                 .attr("fill", "none")
                 
                 .attr("stroke", "#ff001e")
                 .attr("stroke-width", 1.5)
                 .attr("stroke-linejoin", "round")
                 .attr("d", d3.line()
                     .curve(d3.curveBasis)
                     .x(function (d) { return x(d[0]); })
                     .y(function (d) { return y(d[1]); })
                 )
            svg2.append("text")
                 .attr("text-anchor", "middle")
                 .attr("x", width / 2 )
                 .attr("y", height + margin.top+25)
                 .text("Delay in ms");

        }
}