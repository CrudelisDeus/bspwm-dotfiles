return {
  "folke/snacks.nvim",
  opts = {
    picker = {
      sources = {
        explorer = {
          hidden = true,  -- показывать .env, .git, .config и т.п.
          ignored = true, -- показывать gitignored
        },
      },
    },
  },
}
