-- Tool pages with `status: in-development` get a notice at the top of the page body, so the
-- status is clear even before the reader reaches the badges.

function Pandoc(doc)
  local status = doc.meta.status and pandoc.utils.stringify(doc.meta.status) or ""
  if status ~= "in-development" then return doc end
  local notice = pandoc.RawBlock("html",
    '<div class="tool-dev-notice" role="note">'
    .. '<span><strong>In development.</strong> This tool has not been released yet.</span>'
    .. '</div>')
  doc.blocks:insert(1, notice)
  return doc
end
