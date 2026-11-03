-- Learning and workshop pages: wraps each table in Bootstrap's .table-responsive, so a table
-- that fits the column looks unchanged and a wider one scrolls sideways inside the column
-- instead of spilling past it. Applied from learn/_metadata.yml and workshops/<name>/_metadata.yml.
-- Quarto can run the filter more than once, so tables already wrapped are left alone.

return {
  traverse = "topdown",
  Div = function(div)
    if div.classes:includes("table-responsive") then
      return nil, false
    end
  end,
  Table = function(tbl)
    return pandoc.Div({ tbl }, pandoc.Attr("", { "table-responsive" })), false
  end
}
