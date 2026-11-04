-- {{< tool-tags >}}: the same badges and tags the tool's card shows on the Software page,
-- built from the page metadata: a badge row ("In development" when `status: in-development`,
-- `form`, "Breedverse" when `ecosystem: breedverse`,
-- "Runs online" when `links.online` is set, then the latest release version from `version`,
-- linking to `version-url`), then `tasks` and `tags`, each tag linking
-- to the Software page filtered by that tag.

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

return {
  ["tool-tags"] = function(args, kwargs, meta)
    local seen, tags = {}, {}
    for _, field in ipairs({ "tasks", "tags" }) do
      for _, value in ipairs(as_list(meta[field])) do
        local tag = pandoc.utils.stringify(value)
        if tag ~= "" and not seen[tag] then
          seen[tag] = true
          table.insert(tags, tag)
        end
      end
    end
    local badges = {}
    if meta.status and pandoc.utils.stringify(meta.status) == "in-development" then
      table.insert(badges, '<span class="hub-badge hub-badge-dev">In development</span>')
    end
    if meta.form then
      table.insert(badges, '<span class="hub-badge">' .. escape_html(pandoc.utils.stringify(meta.form)) .. '</span>')
    end
    if meta.ecosystem and pandoc.utils.stringify(meta.ecosystem) == "breedverse" then
      table.insert(badges, '<span class="hub-badge hub-badge-eco">Breedverse</span>')
    end
    if meta.links and meta.links.online then
      table.insert(badges, '<span class="hub-badge hub-badge-online">Runs online</span>')
    end
    if meta.version then
      local version = escape_html(pandoc.utils.stringify(meta.version))
      local date = meta["version-date"] and pandoc.utils.stringify(meta["version-date"]) or ""
      local title = date ~= "" and ("Latest release, " .. escape_html(date)) or "Version"
      if meta["version-url"] then
        table.insert(badges, string.format('<a class="hub-badge hub-badge-version" href="%s" title="%s">v%s</a>',
          escape_html(pandoc.utils.stringify(meta["version-url"])), title, version))
      else
        table.insert(badges, string.format('<span class="hub-badge hub-badge-version" title="%s">v%s</span>', title, version))
      end
    end
    local badge_row = #badges > 0
      and ('<div class="hub-badges tool-badges">' .. table.concat(badges) .. '</div>') or ""

    if #tags == 0 then return pandoc.RawBlock("html", badge_row) end

    local links = {}
    for _, tag in ipairs(tags) do
      table.insert(links, string.format('<a class="tool-tag" href="../software.html?tag=%s">%s</a>',
        encode_query(tag), escape_html(tag)))
    end
    return pandoc.RawBlock("html", badge_row ..
      '<div class="tool-tags" aria-label="Tags">' .. table.concat(links) .. '</div>')
  end
}
