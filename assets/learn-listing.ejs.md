```{=html}
<div class="learn-listing-grid list">
<% for (const item of items) {
     const software = Array.isArray(item.software) ? item.software : (item.software ? [item.software] : []);
     const categories = Array.isArray(item.categories) ? item.categories : (item.categories ? [item.categories] : []);
     const learningType = item['learning-type'] || 'Learning material';
     const level = item.level || '';
%>
  <article class="learn-listing-card" <%= metadataAttrs(item) %>>
    <% if (item.image) { %>
    <a class="learn-listing-image" href="<%- item.path %>" aria-label="Open <%- item.title %>">
      <img src="<%- item.image %>" alt="<%- item['image-alt'] || '' %>" loading="lazy">
    </a>
    <% } %>

    <div class="learn-listing-body">
      <div class="learn-card-badges" aria-label="Learning material metadata">
        <span class="learn-badge learn-badge-type listing-learning-type"><%- learningType %></span>
        <% for (const tool of software) { %>
        <span class="learn-badge learn-badge-software listing-software"><%- tool %></span>
        <% } %>
        <% if (level) { %>
        <span class="learn-badge learn-badge-level listing-level"><%- level %></span>
        <% } %>
      </div>

      <h3 class="learn-listing-title">
        <a href="<%- item.path %>" class="listing-title"><%- item.title %></a>
      </h3>

      <% if (item.description) { %>
      <p class="learn-listing-description listing-description"><%- item.description %></p>
      <% } %>

      <% if (categories.length) { %>
      <div class="learn-card-topics" aria-label="Topics">
        <% for (const category of categories) { %>
        <span class="learn-topic-tag listing-categories"><%- category %></span>
        <% } %>
      </div>
      <% } %>

      <a class="learn-card-open" href="<%- item.path %>">Open <%- learningType.toLowerCase() %> <span aria-hidden="true">→</span></a>
    </div>
  </article>
<% } %>
</div>
```
