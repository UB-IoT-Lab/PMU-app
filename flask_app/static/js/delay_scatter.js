   function delay_scatter(data1) {
    
    var formatAsInteger = d3.format(",");
    // set the dimensions and margins of the graph
    var margin = { top: 10, right: 30, bottom: 50, left: 100 };
            width = 700 - margin.left - margin.right,
            height = 450 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg1 = d3.select("#my_dataviz")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    var brush = d3.brush().extent([[0, 0], [width, height]]).on("end", brushended),
            idleTimeout,
            idleDelay = 350;
    var clip = svg1.append("defs").append("svg:clipPath")
            .attr("id", "clip")
            .append("svg:rect")
            .attr("width", width)
            .attr("height", height)
            .attr("x", 0)
            .attr("y", 0); 
    var xExtent = [0, (data1).length / 2];
    var yExtent = d3.extent(data1, function (d) { return d.delay; });
        //console.log((data).length)
        // Add X axis
        var scatter = svg1.append('g')
                .attr("id", "scatterplot")
                .attr("clip-path", "url(#clip)")
        var x = d3.scaleLinear()
            .domain(d3.extent(data1, function (d) { return d.pakno; })).nice()
            .range([0, width]);
        var xAxis = d3.axisBottom(x).ticks(12);
        
        svg1.append("g")
            .attr("transform", "translate(0," + height + ")")
            .attr('id', "axis--x")
            .call(xAxis);

        // Add Y axis
        var y = d3.scaleLinear()
            .domain([0,d3.max(data1, function (d) { return d.delay; })*2]).nice()
            .range([height, 0]);
        var yAxis = d3.axisLeft(y).ticks(12 * height / width);
        svg1.append("g")
            .attr('id', "axis--y")
            .call(yAxis);

        // Add a tooltip div. Here I define the general feature of the tooltip: stuff that do not depend on the data point.
        // Its opacity is set to 0: we don't see it by default.
        var tooltip = d3.select("#my_dataviz")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "1px")
            .style("border-radius", "5px")
            .style("padding", "10px")



        // A function that change this tooltip when the user hover a point.
        // Its opacity is set to 1: we can now see it. Plus it set the text and position of tooltip depending on the datapoint (d)
        // var mouseover = function (d) {
        //     tooltip
        //         .style("opacity", 1)
        //         .html("<b>Delay</b>: " + d.delay)
        //         .style("left", (d3.event.pageX + 5) + "px") // It is important to put the +90: other wise the tooltip is exactly where the point is an it creates a weird effect
        //         .style("top", (d3.event.pageY + 5) + "px")
        // }

        // var mousemove = function (d) {
        //     tooltip
        //         .style("opacity", 1)
        //         .html("<b>Delay</b>: " + d.delay)
        //         .style("left", (d3.event.pageX + 5) + "px") // It is important to put the +90: other wise the tooltip is exactly where the point is an it creates a weird effect
        //         .style("top", (d3.event.pageY+5) + "px")
        // }

        // // A function that change this tooltip when the leaves a point: just need to set opacity to 0 again
        // var mouseleave = function (d) {
        //     tooltip
        //         .transition()
        //         .duration(100)
        //         .style("opacity", 0)
        // }
        svg1.append("text")
            .attr("text-anchor", "middle")
            .attr("x", width / 2 )
            .attr("y", height + margin.top + 25)
            .text("Packet No");

        // Y axis label:
        svg1.append("text")
            .attr("text-anchor", "end")
            .attr("transform", "rotate(-90)")
            .attr("y", -margin.left + 60)
            .attr("x", -margin.top - height / 2 + 20)
            .text("Delay in Sec ")

        var dotcolor = d3.scaleOrdinal()
            .domain([1, 2])
            .range(["#0a74bf", "#ff001e"])
        var dotr = d3.scaleOrdinal()
            .domain([1, 2])
            .range([2, 1.5])
        var dotop = d3.scaleOrdinal()
            .domain([1, 2])
            .range([0.5, 1])
        // Add dots
        

        scatter.selectAll(".dot")
            .data(data1) // the .filter part is just to keep a few dots on the chart, not all of them
            .enter()
            .append("circle")
            .attr("class", "dot")
            .attr("cx", function (d) { return x(d.pakno); })
            .attr("cy", function (d) { return y(d.delay); })
            .attr("r", function (d) { return dotr(d.type) })
            .style("fill", function (d) { return dotcolor(d.type) } )
            .style("opacity", function (d) { return dotop(d.type) })
            //.style("stroke", "white")
            // .on("mouseover", mouseover)
            // .on("mousemove", mousemove)
            // .on("mouseleave", mouseleave)
        
        scatter.append("g")
                .attr("class", "brush")
                .call(brush);
        
        function brushended() {

                var s = d3.event.selection;
                if (!s) {
                    if (!idleTimeout) return idleTimeout = setTimeout(idled, idleDelay);
                    x.domain(d3.extent(data1, function (d) { return d.pakno; })).nice();
                    y.domain([0, d3.max(data1, function (d) { return d.delay; }) * 2]).nice();
                } else {

                    x.domain([s[0][0], s[1][0]].map(x.invert, x));
                    y.domain([s[1][1], s[0][1]].map(y.invert, y));
                    scatter.select(".brush").call(brush.move, null);
                }
                zoom();
            }

            function idled() {
                idleTimeout = null;
            }

            function zoom() {

                var t = scatter.transition().duration(200);
                svg1.select("#axis--x").transition(t).call(xAxis);
                svg1.select("#axis--y").transition(t).call(yAxis);
                scatter.selectAll("circle").transition(t)
                    .attr("cx", function (d) { return x(d.pakno); })
                    .attr("cy", function (d) { return y(d.delay); });
            }
        }