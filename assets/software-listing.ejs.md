```{=html}
<%
// Controlled vocabulary for software pages. Rendering fails on any value not listed here,
// so new domains, types, or tasks are added deliberately (see CONTRIBUTING.md).
const DOMAINS = [
  'Genomic Analysis',
  'Data Management',
  'Pedigree & Mating',
  'Markers & Haplotypes',
  'Phenomics',
  'Utilities'  // keep last: its section sits just above "In development"
];
// Domains of simpler tools, always shown as compact rows without logos, whatever the view.
const COMPACT_DOMAINS = ['Utilities'];
const FORMS = ['Web app', 'R Shiny app', 'R package', 'Python package', 'Mobile app'];
const TASKS = [
  'GWAS', 'Genomic selection', 'Population structure', 'Ploidy', 'CNV',
  'Microhaplotypes', 'MADC processing',
  'Mate allocation', 'Kinship', 'Pedigree', 'Parentage', 'Ancestry'
];
const MAX_TASKS = 3;
// Release status. In-development tools get their own section at the bottom of the page,
// an "In development" badge, and a notice on their tool page (assets/tool-status.lua).
const STATUSES = { 'released': 'Released', 'in-development': 'In development' };

const asArray = (value) => Array.isArray(value) ? value : (value ? [value] : []);
const encoded = (value) => encodeURIComponent(JSON.stringify(value));
const initials = (name) => (String(name).match(/[A-Z]/g) || [String(name).slice(0, 2)]).join('').slice(0, 2);

for (const item of items) {
  const where = `software page "${item.title}"`;
  if (!DOMAINS.includes(item.domain)) throw new Error(`${where}: domain "${item.domain}" is not one of ${DOMAINS.join(', ')}`);
  if (!FORMS.includes(item.form)) throw new Error(`${where}: form "${item.form}" is not one of ${FORMS.join(', ')}`);
  if (!(item.status in STATUSES)) throw new Error(`${where}: status "${item.status}" is not one of ${Object.keys(STATUSES).join(', ')}`);
  const tasks = asArray(item.tasks);
  if (tasks.length > MAX_TASKS) throw new Error(`${where}: list at most ${MAX_TASKS} tasks`);
  for (const task of tasks) {
    if (!TASKS.includes(task)) throw new Error(`${where}: task "${task}" is not in the task list in assets/software-listing.ejs.md`);
  }
}

// Every domain is listed in the sidebar (empty ones show a count of 0); only domains
// with released tools get a section on the page. In-development tools all go in one
// "In development" section after the released domains.
const sorted = items.slice().sort((a, b) => String(a.title).localeCompare(String(b.title)));
const usedDomains = DOMAINS.filter((domain) => sorted.some((item) => item.domain === domain));
const released = sorted.filter((item) => item.status === 'released');
const inDevelopment = sorted
  .filter((item) => item.status === 'in-development')
  .sort((a, b) => DOMAINS.indexOf(a.domain) - DOMAINS.indexOf(b.domain) || String(a.title).localeCompare(String(b.title)));
const usedForms = FORMS.filter((form) => sorted.some((item) => item.form === form));
%>
<% function renderCard(item, compact) {
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
        data-status="<%= STATUSES[item.status] %>"
        data-domain="<%= item.domain %>"
        data-form="<%= item.form %>"
        data-online="<%= links.online ? 'true' : 'false' %>"
        data-tasks="<%- encoded(tasks) %>"
        data-tags="<%- encoded(tags) %>"
        data-search="<%- encoded(searchText) %>">
        <div class="hub-card-head">
<% if (compact) { %>
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
          <button type="button" class="hub-tag" data-tag="<%= tag %>" aria-pressed="false"><%= tag %></button>
<% } %>
        </div>
<% } %>
      </article>
<% } %>
<div class="hub-catalog" data-domains="<%- encoded(DOMAINS) %>" data-forms="<%- encoded(usedForms) %>" data-tasks="<%- encoded(TASKS) %>" data-statuses="<%- encoded(Object.values(STATUSES)) %>">
<% for (const domain of usedDomains) {
     const group = released.filter((item) => item.domain === domain);
     if (!group.length) continue;
     const groupId = 'domain-' + domain.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
     const compact = COMPACT_DOMAINS.includes(domain);
%>
  <section class="hub-group<%= compact ? ' hub-compact-group' : '' %>" data-domain="<%= domain %>" aria-labelledby="<%- groupId %>">
    <div class="hub-group-head">
      <h2 id="<%- groupId %>" class="anchored"><%= domain %></h2>
      <span class="hub-group-count"><%= group.length %></span>
    </div>
    <div class="hub-items">
<% for (const item of group) { renderCard(item, compact); } %>
    </div>
  </section>
<% } %>
<% if (inDevelopment.length) { %>
  <section class="hub-group hub-dev-group" aria-labelledby="in-development">
    <div class="hub-group-head">
      <h2 id="in-development" class="anchored">In development</h2>
      <span class="hub-group-count"><%= inDevelopment.length %></span>
    </div>
    <div class="hub-items">
<% for (const item of inDevelopment) { renderCard(item); } %>
    </div>
  </section>
<% } %>
</div>
```
