if vim.g.loaded_example_plugin == 1 then
  return
end
vim.g.loaded_example_plugin = 1

vim.api.nvim_create_user_command("ExampleHello", function(command)
  require("example").hello(command.args)
end, {
  nargs = "?",
  desc = "Show the example plugin greeting",
})
