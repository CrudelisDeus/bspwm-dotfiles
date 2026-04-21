local map = vim.keymap.set

-- Save current file
map("n", "<leader>w", ":w<cr>", { desc = "Save file", remap = true })
