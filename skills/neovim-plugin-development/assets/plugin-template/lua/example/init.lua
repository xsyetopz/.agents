local M = {}

local config = require("example.config").resolve()

function M.setup(options)
  config = require("example.config").resolve(options)
end

function M.hello(name)
  vim.notify(string.format("%s: hello %s", config.prefix, name ~= "" and name or "workspace"))
end

return M
