<%
// One software card, shared by the Software catalog (assets/software-listing.ejs.md) and the
// featured tools on the home page (assets/featured-software.ejs.md).
//   compact: no logo (Utilities rows)
//   tagHref: tags become links to the catalog filtered by that tag, for pages without filters
//   statuses: the catalog's STATUSES map (status -> filter label); pages without the Status
//             filter (home featured software) don't pass it and get the raw status
const statusLabels = typeof statuses !== 'undefined' ? statuses : {};
const asArray = (value) => Array.isArray(value) ? value : (value ? [value] : []);
const encoded = (value) => encodeURIComponent(JSON.stringify(value));
const initials = (name) => (String(name).match(/[A-Z]/g) || [String(name).slice(0, 2)]).join('').slice(0, 2);
const isCompact = typeof compact !== 'undefined' && compact;
const tagLink = typeof tagHref !== 'undefined' ? tagHref : '';
const tasks = asArray(item.tasks);
const tags = asArray(item.tags).filter((tag) => !tasks.includes(tag));
const allTags = tasks.concat(tags);
const links = item.links || {};
const searchText = [item.title, item.description, item.domain, item.form, item.version ? 'v' + item.version : '']
  .concat(allTags)
  .filter(Boolean)
  .join(' ');
%>
      <article class="hub-card<%= item.status === 'in-development' ? ' is-dev' : '' %>"
        data-status="<%= statusLabels[item.status] || item.status %>"
        data-domain="<%= item.domain %>"
        data-form="<%= item.form %>"
        data-online="<%= links.online ? 'true' : 'false' %>"
        data-tasks="<%- encoded(tasks) %>"
        data-tags="<%- encoded(tags) %>"
        data-search="<%- encoded(searchText) %>">
        <div class="hub-card-head">
<% if (isCompact) { %>
<% } else if (item.image) { %>
          <img class="hub-logo<%= item['image-wide'] ? ' wide' : '' %>" src="<%- item.image %>" alt="" loading="lazy">
<% } else { %>
          <span class="hub-logo hub-logo-fallback" aria-hidden="true"><%= initials(item.title) %></span>
<% } %>
          <div class="hub-card-title">
            <span class="hub-domain-label"><%= item.domain %></span>
            <h3><a class="hub-card-link" href="<%- item.path %>"><%= item.title %></a><% if (item.version) { %> <span class="hub-version" title="<%= item['version-date'] ? 'Latest release, ' + item['version-date'] : 'Version' %>">v<%= item.version %></span><% } %></h3>
          </div>
        </div>
        <div class="hub-card-mid">
          <div class="hub-badges">
<% if (item.status === 'in-development') { %>
            <span class="hub-badge hub-badge-dev">In development</span>
<% } %>
            <span class="hub-badge"><%= item.form %></span>
<% if (item.ecosystem === 'breedverse') { %>
            <span class="hub-badge hub-badge-eco">Breedverse</span>
<% } %>
<% if (links.online) { %>
            <span class="hub-badge hub-badge-online">Runs online</span>
<% } %>
          </div>
<% if (item.description) { %>
          <p class="hub-desc"><%= item.description %></p>
<% } %>
        </div>
<% if (allTags.length) { %>
        <div class="hub-tags" aria-label="Tags">
<% for (const tag of allTags) { %>
<% if (tagLink) { %>
          <a class="hub-tag" href="<%- tagLink + encodeURIComponent(tag) %>"><%= tag %></a>
<% } else { %>
          <button type="button" class="hub-tag" data-tag="<%= tag %>" aria-pressed="false"><%= tag %></button>
<% } %>
<% } %>
        </div>
<% } %>
      </article>
