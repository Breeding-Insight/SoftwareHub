```{=html}
<%
const externalItems = [
  {
    title: 'Estimate copy number in alfalfa with Qploidy2',
    description: 'Use Qploidy2 with DArTag data to estimate ploidy, aneuploidy, and large-scale copy-number variation.',
    categories: ['Ploidy & Dosage', 'Genotype Data'],
    image: 'assets/tutorial-qploidy.svg',
    'image-alt': 'Ploidy and copy-number variation tutorial.',
    order: 30,
    'learning-type': 'Tutorial',
    author: 'Cristiane H. Taniguti',
    software: ['Qploidy2'],
    level: 'Intermediate',
    keywords: ['alfalfa', 'CNV', 'DArTag', 'copy number', 'aneuploidy'],
    path: 'https://breeding-insight.github.io/Qploidy2/Qploidy_alfalfa_tutorial.html',
    external: true
  }
];

const learningItems = items
  .concat(externalItems)
  .sort((a, b) => (Number(a.order) || 999) - (Number(b.order) || 999));

const asArray = (value) => Array.isArray(value) ? value : (value ? [value] : []);
const encoded = (value) => encodeURIComponent(JSON.stringify(value));
%>
<div class="hub-items learn-listing-grid">
<% for (const item of learningItems) {
     const software = asArray(item.software);
     const categories = asArray(item.categories);
     const keywords = asArray(item.keywords);
     const learningType = item['learning-type'] || 'Learning material';
     const level = item.level || '';
     const author = Array.isArray(item.author)
       ? item.author.map((entry) => typeof entry === 'string' ? entry : entry.name).filter(Boolean).join(', ')
       : (typeof item.author === 'object' ? item.author.name : item.author) || '';
     const isExternal = item.external === true;
     const searchText = [item.title, item.description, learningType, level, author, isExternal ? 'External' : '']
       .concat(software, categories, keywords)
       .filter(Boolean)
       .join(' ');
     const shownSoftware = software.slice(0, 3);
%>
  <article class="hub-card learn-listing-card"
    data-learn-type="<%- encoded([learningType]) %>"
    data-learn-topic="<%- encoded(categories) %>"
    data-learn-software="<%- encoded(software) %>"
    data-learn-level="<%- encoded(level ? [level] : []) %>"
    data-learn-search="<%- encoded(searchText) %>">
<% if (item.image) { %>
    <div class="hub-card-image">
      <img src="<%- item.image %>" alt="<%- item['image-alt'] || '' %>" loading="lazy">
    </div>
<% } %>
    <div class="hub-badges" aria-label="Learning material metadata">
      <span class="hub-badge hub-badge-eco"><%- learningType %></span>
<% if (isExternal) { %>
      <span class="hub-badge">External</span>
<% } %>
<% if (level) { %>
      <span class="hub-badge"><%- level %></span>
<% } %>
<% for (const tool of shownSoftware) { %>
      <span class="hub-badge">Uses <%- tool %></span>
<% } %>
<% if (software.length > shownSoftware.length) { %>
      <span class="hub-badge">+<%- software.length - shownSoftware.length %></span>
<% } %>
    </div>
    <h3><a class="hub-card-link<%= isExternal ? '' : ' no-external' %>" href="<%- item.path %>"<% if (isExternal) { %> target="_blank" rel="noopener"<% } %>><%- item.title %><% if (isExternal) { %><span class="visually-hidden"> (external tutorial)</span><% } %></a></h3>
<% if (item.description) { %>
    <p class="hub-desc"><%- item.description %></p>
<% } %>
<% if (categories.length) { %>
    <div class="hub-tags" aria-label="Topics">
<% for (const category of categories) { %>
      <button type="button" class="hub-tag" data-facet="topic" data-value="<%= category %>" aria-pressed="false"><%- category %></button>
<% } %>
    </div>
<% } %>
    <span class="hub-card-open" aria-hidden="true">Open <%- learningType.toLowerCase() %> <%= isExternal ? '↗' : '→' %></span>
  </article>
<% } %>
</div>
```
