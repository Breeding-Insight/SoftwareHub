-- Release-note pages (news/*.qmd): builds the package badge for the title strip, linking to
-- the News page filtered by that package. Done here rather than in the title template
-- because Pandoc templates can't URL-encode, so a name with a space, & or + would break the
-- link. assets/release-partials/title-block.html places it as $release-packages$.

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
  for _, category in ipairs(as_list(meta.categories)) do
    local package = pandoc.utils.stringify(category)
    table.insert(badges, string.format(
      '<a class="hub-badge hub-badge-eco release-package" href="../news.html?package=%s">%s</a>',
      encode_query(package), escape_html(package)))
  end
  if #badges > 0 then
    meta["release-packages"] = pandoc.RawInline("html",
      '<div class="hub-badges" aria-label="Package">' .. table.concat(badges) .. '</div>')
  end
  return meta
end
