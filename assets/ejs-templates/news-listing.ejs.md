```{=html}
<%
// News page: one row per release, newest first (sorted by the listing in news.qmd).
// assets/news-filter.html builds the Package filter from data-package.
const asArray = (value) => Array.isArray(value) ? value : (value ? [value] : []);
const encoded = (value) => encodeURIComponent(JSON.stringify(value));
%>
<div class="hub-items news-list">
<% for (const item of items) {
     const packages = asArray(item.categories);
     const searchText = [item.title, item.description, item.date].concat(packages).filter(Boolean).join(' ');
%>
  <article class="hub-card news-item"
    data-package="<%- encoded(packages) %>"
    data-search="<%- encoded(searchText) %>">
<% if (item.image) { %>
    <img class="hub-logo" src="<%- item.image %>" alt="" loading="lazy">
<% } %>
    <div class="news-item-body">
      <div class="news-item-meta">
<% for (const pkg of packages) { %>
        <span class="hub-domain-label"><%= pkg %></span>
<% } %>
<% if (item.date) { %>
        <time class="news-date"><%= item.date %></time>
<% } %>
      </div>
      <h3><a class="hub-card-link" href="<%- item.path %>"><%= item.title %></a></h3>
<% if (item.description) { %>
      <p class="hub-desc"><%= item.description %></p>
<% } %>
    </div>
  </article>
<% } %>
</div>
```
