function arriv_scatter(data){

    
    // set the dimensions and margins of the graph
    var margin = { top: 10, right: 30, bottom: 50, left: 100 },
            width = 700 - margin.left - margin.right,
            height = 450 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg3 = d3.select("#arriv_scatter")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");
    plotgraph(data)
    //Read the data
    function plotgraph(data) {
        //console.log((data).length)
        // Add X axis
        var x = d3.scaleLinear()
            .domain([d3.min(data, d => d.ard)-0.1, d3.max(data, d => d.serv)])
            .range([0, width]);
        svg3.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        // Add Y axis
        var y = d3.scaleLinear()
            .domain([0, 100])
            .range([height, 0]);
        svg3.append("g")
            .call(d3.axisLeft(y)
                    .ticks(0));

        // Add a tooltip div. Here I define the general feature of the tooltip: stuff that do not depend on the data point.
        // Its opacity is set to 0: we don't see it by default.
        var tooltip = d3.select("#arriv_scatter")
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
        var mouseover = function (x) {
            tooltip
                .style("opacity", 1)
                .html("<b>Time </b>: " + x)
                .style("left", (d3.event.pageX + 5) + "px") // It is important to put the +90: other wise the tooltip is exactly where the point is an it creates a weird effect
                .style("top", (d3.event.pageY+5) + "px")
        }

        var mousemove = function (x) {
            tooltip
                .style("opacity", 1)
                .html("<b>Time </b>: " + x)
                .style("left", (d3.event.pageX + 5) + "px") // It is important to put the +90: other wise the tooltip is exactly where the point is an it creates a weird effect
                .style("top", (d3.event.pageY + 5) + "px")
        }

        // A function that change this tooltip when the leaves a point: just need to set opacity to 0 again
        var mouseleave = function (x) {
            tooltip
                .style("opacity", 0)
        }
        svg3.append("text")
            .attr("text-anchor", "middle")
            .attr("x", width / 2 )
            .attr("y", height + margin.top + 25)
            .text("Time in Sec");

        // Y axis label:
        svg3.append("text")
            .attr("text-anchor", "middle")
            .attr("transform", "rotate(-90)")
            .attr("y", -margin.left + 60)
            .attr("x",  -y(70) )
            .text("Time-Stamp")
        svg3.append("text")
            .attr("text-anchor", "middle")
            .attr("transform", "rotate(-90)")
            .attr("y", -margin.left + 60)
            .attr("x", -y(30))
            .text("Arrival")

        var dotcolor = d3.scaleOrdinal()
            .domain([1, 2])
            .range(["green", "red"])
        var dotr = d3.scaleOrdinal()
            .domain([1, 2])
            .range([2, 1.5])
        var dotop = d3.scaleOrdinal()
            .domain([1, 2])
            .range([0.5, 1])
        // Add dots
        svg3.append('g')
            .selectAll("dot")
            .data(data) // the .filter part is just to keep a few dots on the chart, not all of them
            .enter()
            .append("circle")
            .attr("cx", function (d) { return x(d.ard); })
            .attr("cy", function (d) { return y(70); })
            .attr("r", function (d) { return dotr(1) })
            .style("fill", function (d) { return dotcolor(1) })
            .style("opacity", function (d) { return dotop(1) })
            .style("stroke", "green")
            .on("mouseover", function (d) { return mouseover(d.ard); } )
            .on("mousemove", function (d) { return mousemove(d.ard); })
            .on("mouseleave", function (d) { return mouseleave(d.ard); })
        
        svg3.append('g')
            .selectAll("dot")
            .data(data) // the .filter part is just to keep a few dots on the chart, not all of them
            .enter()
            .append("circle")
            .attr("cx", function (d) { return x(d.serv); })
            .attr("cy", function (d) { return y(30); })
            .attr("r", function (d) { return dotr(2) })
            .style("fill", function (d) { return dotcolor(2) })
            .style("opacity", function (d) { return dotop(2) })
            .style("stroke", "red")
            .on("mouseover", function (d) { return mouseover(d.serv); })
            .on("mousemove", function (d) { return mousemove(d.serv); })
            .on("mouseleave", function (d) { return mouseleave(d.serv); })
            

    }
}