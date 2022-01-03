import * as d3 from 'd3'

const label = d => d.name

const tree = d3.tree
const [width, height] = [900, 300]
const [padding, r, fill, stroke, strokeOpacity, strokeWidth] = [1, 10, '#999', '#555', 0.4, 1.5]
const halo = '#fff'
const haloWidth = 3

const title = null
const sort = null
const link = null
const strokeLinecap = null
const strokeLinejoin = null

const strokeColor = '#1867F7'

export default class Hierarchy {
    constructor(data) {
        const root = d3.hierarchy(data);

        // Compute labels and titles.
        const descendants = root.descendants();
        const L = label == null ? null : descendants.map(d => label(d.data, d));

        // Sort the nodes.
        if (sort != null) root.sort(sort);

        // Compute the layout.
        const dx = 90;
        const dy = width / (root.height + padding);
        
        const res = tree().nodeSize([dx, dy])(root);
        console.log(res)

        // Center the tree.
        let x0 = Infinity;
        let x1 = -x0;
        root.each(d => {
            if (d.x > x1) x1 = d.x;
            if (d.x < x0) x0 = d.x;
        });

        // Compute the default height.
        if (height === undefined) height = x1 - x0 + dx * 2;

        const svg = d3.create("svg")
            .attr("viewBox", [-dy * padding / 2, x0 - dx, width, height])
            .attr("width", width)
            .attr("height", height)
            .attr("style", "max-width: 100%; height: 300; height: intrinsic;")
            .attr("font-family", "sans-serif")
            .attr("font-size", 10);

        svg.append("g")
            .attr("fill", "none")
            .attr("stroke", stroke)
            .attr("stroke-opacity", strokeOpacity)
            .attr("stroke-linecap", strokeLinecap)
            .attr("stroke-linejoin", strokeLinejoin)
            .attr("stroke-width", strokeWidth)
            .selectAll("path")
            .data(root.links())
            .join("path")
            .attr('class', 'flow')
            .attr("d", d3.linkHorizontal()
                .x(d => d.y)
                .y(d => d.x));

        const node = svg.append("g")
            .selectAll("a")
            .data(root.descendants())
            .join("a")
            .attr("xlink:href", link == null ? null : d => link(d.data, d))
            .attr("target", link == null ? null : linkTarget)
            .attr("transform", d => `translate(${d.y},${d.x - 15})`);

        node.append("rect")
            .attr("fill", '#fff')
            .attr("stroke", strokeColor)
            .attr("rx", 2)
            .attr("width", 100)
            .attr("height", 50)
            .attr("x", 0)
            .attr("y", -10)

        if (title != null) node.append("title")
            .text(d => title(d.data, d));

        if (L) node.append("text")
            .attr("dy", "0.32em")
            // .attr("x", d => d.children ? -6 : 6)
            .attr("x", 50)
            .attr("text-anchor", "middle")
            // .attr("text-anchor", d => d.children ? "end" : "start")
            .text((d, i) => L[i])
            .call(text => text.clone(true))
            .attr("fill", "none")
            .attr("stroke", halo)
            .attr("stroke-width", haloWidth);
        
        document.querySelector('#graph-container').innerHTML = ''
        document.querySelector('#graph-container').append(svg.node())
    }
}