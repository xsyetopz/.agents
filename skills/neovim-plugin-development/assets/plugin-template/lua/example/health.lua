local M = {}

function M.check()
  vim.health.start("example.nvim")

  if vim.fn.has("nvim-0.12") == 1 then
    vim.health.ok("Neovim 0.12 or newer")
  else
    vim.health.error("Neovim 0.12 or newer is required")
  end

  if vim.fn.executable("__OPTIONAL_EXECUTABLE__") == 1 then
    vim.health.ok("Optional executable is available")
  else
    vim.health.warn("Optional executable is unavailable", {
      "Install it only if the optional integration is needed.",
    })
  end
end

return M
