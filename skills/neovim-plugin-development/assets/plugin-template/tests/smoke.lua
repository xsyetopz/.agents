local example = require("example")
local root = vim.fn.fnamemodify(debug.getinfo(1, "S").source:sub(2), ":p:h:h")

example.setup({ prefix = "Test" })
assert(vim.fn.exists(":ExampleHello") == 2, "ExampleHello command was not registered")

vim.cmd("checkhealth example")
vim.cmd("helptags " .. vim.fn.fnameescape(root .. "/doc"))

vim.cmd("qa!")
