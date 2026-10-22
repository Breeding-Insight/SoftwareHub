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
<% for (const item of group) { partial('software-card.ejs.md', { item, compact, statuses: STATUSES }); } %>
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
<% for (const item of inDevelopment) { partial('software-card.ejs.md', { item, compact: false, statuses: STATUSES }); } %>
    </div>
  </section>
<% } %>
</div>
```
