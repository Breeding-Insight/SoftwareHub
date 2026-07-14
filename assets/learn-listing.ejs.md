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
<div class="learn-listing-grid">
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
%>
  <article class="learn-listing-card"
    data-learn-type="<%- encoded([learningType]) %>"
    data-learn-topic="<%- encoded(categories) %>"
    data-learn-software="<%- encoded(software) %>"
    data-learn-level="<%- encoded(level ? [level] : []) %>"
    data-learn-search="<%- encoded(searchText) %>">
    <a class="learn-listing-link<%= isExternal ? '' : ' no-external' %>" href="<%- item.path %>"<% if (isExternal) { %> target="_blank" rel="noopener"<% } %>>
<% if (item.image) { %>
    <div class="learn-listing-image">
      <img src="<%- item.image %>" alt="<%- item['image-alt'] || '' %>" loading="lazy">
    </div>
<% } %>

    <div class="learn-listing-body">
      <div class="learn-card-badges" aria-label="Learning material metadata">
        <span class="learn-badge learn-badge-type"><%- learningType %></span>
<% if (isExternal) { %>
        <span class="learn-badge learn-badge-external">External</span>
<% } %>
<% const shownSoftware = software.slice(0, 3); %>
<% for (const tool of shownSoftware) { %>
        <span class="learn-badge learn-badge-software">Uses <%- tool %></span>
<% } %>
<% if (software.length > shownSoftware.length) { %>
        <span class="learn-badge learn-badge-more">+<%- software.length - shownSoftware.length %></span>
<% } %>
<% if (level) { %>
        <span class="learn-badge learn-badge-level"><%- level %></span>
<% } %>
      </div>

      <div class="learn-listing-title" role="heading" aria-level="3">
        <%- item.title %><% if (isExternal) { %><span class="visually-hidden"> (external tutorial)</span><% } %>
      </div>

<% if (item.description) { %>
      <p class="learn-listing-description"><%- item.description %></p>
<% } %>

<% if (categories.length) { %>
      <div class="learn-card-topics" aria-label="Topics">
<% for (const category of categories) { %>
        <span class="learn-topic-tag"><%- category %></span>
<% } %>
      </div>
<% } %>

      <span class="learn-card-open" aria-hidden="true">Open <%- learningType.toLowerCase() %> <%= isExternal ? '↗' : '→' %></span>
    </div>
    </a>
  </article>
<% } %>
</div>
```
