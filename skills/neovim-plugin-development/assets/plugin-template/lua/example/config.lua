local M = {}

local defaults = {
  prefix = "Example",
}

function M.resolve(user)
  vim.validate("config", user or {}, "table")
  return vim.tbl_deep_extend("force", {}, defaults, user or {})
end

return M
