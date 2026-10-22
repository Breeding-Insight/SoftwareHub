```{=html}
<%
// Featured tools on the home page: the same cards as the Software catalog
// (assets/software-card.ejs.md), in the order listed in index.qmd. Tags link to the
// catalog filtered by that tag.
%>
<div class="hub-items">
<% for (const item of items) { partial('software-card.ejs.md', { item, compact: false, tagHref: 'software.html?tag=' }); } %>
</div>
```
