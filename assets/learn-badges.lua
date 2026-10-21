-- Learning pages (learn/*.qmd): builds the title strip's badge row and topic tags from the
-- page metadata, the same badges the page's card shows on the Learn page:
-- `learning-type`, `level`, then "Uses <tool>" for each `software` entry. `categories`
-- become topic tags linking to the Learn page filtered by that topic.
-- assets/learn-partials/title-block.html places them as $learn-badges$ and $learn-topics$.

local function as_list(value)
  if value == nil then return {} end
  if pandoc.utils.type(value) == "List" then return value end
  return { value }
end

local function escape_html(text)
  return (text:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

local function encode_query(text)
  return (text:gsub("[^%w%-_%.~]", function(char)
    return string.format("%%%02X", string.byte(char))
  end))
end

function Meta(meta)
  local badges = {}
  if meta["learning-type"] then
    table.insert(badges, '<span class="hub-badge hub-badge-eco">'
      .. escape_html(pandoc.utils.stringify(meta["learning-type"])) .. '</span>')
  end
  if meta.level then
    table.insert(badges, '<span class="hub-badge">' .. escape_html(pandoc.utils.stringify(meta.level)) .. '</span>')
  end
  for _, tool in ipairs(as_list(meta.software)) do
    table.insert(badges, '<span class="hub-badge">Uses ' .. escape_html(pandoc.utils.stringify(tool)) .. '</span>')
  end
  if #badges > 0 then
    meta["learn-badges"] = pandoc.RawInline("html",
      '<div class="hub-badges" aria-label="Learning material details">' .. table.concat(badges) .. '</div>')
  end

  local topics = {}
  for _, category in ipairs(as_list(meta.categories)) do
    local topic = pandoc.utils.stringify(category)
    table.insert(topics, string.format('<a class="tool-tag" href="../learn.html?topic=%s#all-learning-materials">%s</a>',
      encode_query(topic), escape_html(topic)))
  end
  if #topics > 0 then
    meta["learn-topics"] = pandoc.RawInline("html",
      '<div class="tool-tags" aria-label="Topics">' .. table.concat(topics) .. '</div>')
  end
  return meta
end
