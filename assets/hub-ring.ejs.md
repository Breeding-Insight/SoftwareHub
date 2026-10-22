```{=html}
<%
// Home hero: the Breeding Insight mark as the hub, with a spoke to each software domain.
// Each domain's tools sit together at the end of its spoke: hex logos tile into a small
// honeycomb; other logos (`image-wide`, e.g. DeltaBreed, or `image-shape: square`, e.g.
// HapApp) get tiles. In-development tools are included; their titles say so. Built from
// software/*.qmd (listing "hub-ring" in index.qmd), so a new tool with an `image` joins its
// domain on the next render. Domain order follows DOMAINS in assets/software-listing.ejs.md.
const DOMAINS = ['Genomic Analysis', 'Data Management', 'Pedigree & Mating', 'Markers & Haplotypes', 'Phenomics', 'Utilities'];
const tools = items
  .filter((item) => item.image)
  .sort((a, b) => String(a.title).localeCompare(String(b.title)));
const groups = DOMAINS
  .map((domain) => ({ domain, tools: tools.filter((item) => item.domain === domain) }))
  .filter((group) => group.tools.length);

// Domains spread evenly around the hub, the first at upper left. Positions are percentages
// of the square hub box, shared by the spokes (SVG viewBox 0–100) and the clusters.
const RADIUS = 36;
const START = -150;

// Honeycomb for pointy-top hexes: rows of two, then one centred below, and so on.
// HEX is the hex height in em (the ring scales its font size with the screen); the width
// is height × √3/2; GAP separates neighbours.
const HEX = 4.6;
const HEX_W = +(HEX * Math.sqrt(3) / 2).toFixed(3);
const GAP = 0.15;
function honeycomb(count) {
  if (!count) return { cells: [], width: 0, height: 0 };
  const cells = [];
  let row = 0;
  while (cells.length < count) {
    const inRow = Math.min(row % 2 === 0 ? 2 : 1, count - cells.length);
    for (let col = 0; col < inRow; col++) {
      const x = inRow === 2 ? (col === 0 ? -(HEX_W + GAP) / 2 : (HEX_W + GAP) / 2) : 0;
      cells.push({ x, y: row * (HEX * 0.75 + GAP * 0.866) });
    }
    row += 1;
  }
  const width = cells.some((cell) => cell.x !== 0) ? 2 * HEX_W + GAP : HEX_W;
  const height = cells[cells.length - 1].y + HEX;
  return { cells: cells.map((cell) => ({ left: +(cell.x + width / 2 - HEX_W / 2).toFixed(3), top: +cell.y.toFixed(3) })), width: +width.toFixed(3), height: +height.toFixed(3) };
}

const isTile = (tool) => tool['image-wide'] || tool['image-shape'] === 'square';
const spots = groups.map((group, index) => {
  const angle = (START + (360 * index) / groups.length) * Math.PI / 180;
  return {
    ...group,
    x: (50 + RADIUS * Math.cos(angle)).toFixed(2),
    y: (50 + RADIUS * Math.sin(angle)).toFixed(2),
    hexes: group.tools.filter((tool) => !isTile(tool)),
    tiles: group.tools.filter(isTile)
  };
});
%>
<nav class="hub-ring" aria-label="Breeding Insight software by domain">
  <svg class="hub-ring-spokes" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true" focusable="false">
<% for (const spot of spots) { %>
    <line x1="50" y1="50" x2="<%= spot.x %>" y2="<%= spot.y %>"></line>
<% } %>
  </svg>
  <div class="hub-ring-center" aria-hidden="true">
    <img src="assets/bi-mark.png" alt="">
  </div>
<% for (const spot of spots) {
     const comb = honeycomb(spot.hexes.length);
%>
  <div class="hub-ring-cluster" style="left: <%= spot.x %>%; top: <%= spot.y %>%;" role="group" aria-label="<%= spot.domain %>">
<% if (spot.hexes.length) { %>
    <div class="hub-comb" style="width: <%= comb.width %>em; height: <%= comb.height %>em;">
<% spot.hexes.forEach((tool, index) => { %>
      <a class="hub-hex" href="<%- tool.path %>" title="<%= tool.title %><%= tool.status === 'in-development' ? ' (in development)' : '' %>" style="left: <%= comb.cells[index].left %>em; top: <%= comb.cells[index].top %>em; width: <%= HEX_W %>em; height: <%= HEX %>em;">
        <span class="hub-hex-shape"><span class="hub-hex-face"><img src="<%- tool.image %>" alt="<%= tool.title %>"></span></span>
      </a>
<% }); %>
    </div>
<% } %>
<% if (spot.tiles.length) { %>
    <div class="hub-tiles">
<% for (const tool of spot.tiles) { %>
    <a class="hub-tile<%= tool['image-wide'] ? ' is-wide' : '' %>" href="<%- tool.path %>" title="<%= tool.title %><%= tool.status === 'in-development' ? ' (in development)' : '' %>">
      <img src="<%- tool.image %>" alt="<%= tool.title %><%= tool.status === 'in-development' ? ' (in development)' : '' %>">
    </a>
<% } %>
    </div>
<% } %>
    <span class="hub-ring-domain"><%= spot.domain %></span>
  </div>
<% } %>
</nav>
<script>
// Make every hex identical. The logo files are drawn as two different hexagon shapes
// (regular ones with side corners at 25%/75% of the height, and taller, flatter-topped ones
// at 21.5%/78.5%), so no amount of stretching makes them tile evenly. Instead each cell is
// an exact regular hexagon drawn in CSS: an outer hex in the logo's own outline colour (the
// border) and an inner hex holding the logo's artwork. This finds each logo's hexagon
// (opaque area at the mid-edge alpha), measures its outline width and colour at the left
// edge, and scales the image so the inside of its outline fills the inner hex. Without
// JavaScript the border uses the hub border colour and the image is shown at cell height.
(() => {
  function fit(img) {
    const h = 600;
    const w = Math.max(1, Math.round(img.naturalWidth * h / img.naturalHeight));
    const canvas = document.createElement("canvas");
    canvas.width = w;
    canvas.height = h;
    const context = canvas.getContext("2d", { willReadFrequently: true });
    context.drawImage(img, 0, 0, w, h);
    let data;
    try {
      data = context.getImageData(0, 0, w, h).data;
    } catch (_error) {
      return; // cross-origin image: keep the default placement
    }
    const alpha = (x, y) => data[(y * w + x) * 4 + 3];
    let left = w, top = h, right = -1, bottom = -1;
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        if (alpha(x, y) >= 128) {
          if (x < left) left = x;
          if (x > right) right = x;
          if (y < top) top = y;
          if (y > bottom) bottom = y;
        }
      }
    }
    if (right < 0) return;
    const boxW = right - left + 1;
    const boxH = bottom - top + 1;

    // Outline: walk in from the left edge at mid height while the colour stays close to the
    // edge colour; that run is the logo's own border.
    const mid = Math.round((top + bottom) / 2);
    const px = (x) => { const k = (mid * w + x) * 4; return [data[k], data[k + 1], data[k + 2]]; };
    const edge = px(left + 2);
    const near = (c) => Math.abs(c[0] - edge[0]) + Math.abs(c[1] - edge[1]) + Math.abs(c[2] - edge[2]) < 60;
    let border = 2;
    while (border < boxW * 0.12 && near(px(left + border))) border += 1;

    // The inside of the logo's outline (its box inset by the border, kept in proportion)
    // fills the inner hex, which is the cell inset by the same fraction on every side.
    const inset = border / boxW;
    const innerLeft = left + boxW * inset;
    const innerTop = top + boxH * inset;
    const innerW = boxW * (1 - 2 * inset);
    const innerH = boxH * (1 - 2 * inset);
    const shape = img.closest(".hub-hex-shape");
    // No template literals here: the listing template engine treats their placeholders as its own.
    shape.style.setProperty("--hex-border", "rgb(" + edge.join(",") + ")");
    Object.assign(img.style, {
      width: (w / innerW * 100).toFixed(4) + "%",
      height: (h / innerH * 100).toFixed(4) + "%",
      left: (-innerLeft / innerW * 100).toFixed(4) + "%",
      top: (-innerTop / innerH * 100).toFixed(4) + "%",
      transform: "none"
    });
  }
  document.querySelectorAll(".hub-hex img").forEach((img) => {
    if (img.complete && img.naturalWidth) fit(img);
    else img.addEventListener("load", () => fit(img), { once: true });
  });
})();
</script>
```
