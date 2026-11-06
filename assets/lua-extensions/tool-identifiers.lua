-- Puts a tool's citation identifiers above its intro text (first in the `.software-header` text
-- column, or at the top of the page without one), as chips linking to their resolvers:
-- `identifiers.doi` (doi.org) and `identifiers.rrid` (SciCrunch). They are nested under
-- `identifiers:` because Quarto prints a top-level `doi` in the title block. Kept apart from the
-- badges and tags below the intro so neither row gets crowded.

local function escape_html(text)
  return (text:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

function Pandoc(doc)
  local idents = doc.meta.identifiers
  if not idents then return nil end

  local ids = {}
  if idents.doi then
    local doi = pandoc.utils.stringify(idents.doi):gsub("^https?://doi%.org/", "")
    table.insert(ids, string.format(
      '<a class="tool-id" href="https://doi.org/%s"><span class="tool-id-label">DOI</span>%s</a>',
      escape_html(doi), escape_html(doi)))
  end
  if idents.rrid then
    local rrid = pandoc.utils.stringify(idents.rrid):gsub("^RRID:", "")
    table.insert(ids, string.format(
      '<a class="tool-id" href="https://scicrunch.org/resolver/RRID:%s"><span class="tool-id-label">RRID</span>%s</a>',
      escape_html(rrid), escape_html(rrid)))
  end
  if #ids == 0 then return nil end

  local row = pandoc.RawBlock("html",
    '<div class="tool-ids" aria-label="Citation identifiers">' .. table.concat(ids) .. '</div>')
  for _, block in ipairs(doc.blocks) do
    if block.t == "Div" and block.classes:includes("software-header") then
      local column = block.content[1]
      if column and column.t == "Div" then
        column.content:insert(1, row)
      else
        block.content:insert(1, row)
      end
      return doc
    end
  end
  doc.blocks:insert(1, row)
  return doc
end
