-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

local map = vim.keymap.set
vim.g.mapleader = ' '
vim.g.maplocalleader = ' '

-- Save current file
map("n", "<leader>w", ":w<cr>", { desc = "Save file", remap = true })
