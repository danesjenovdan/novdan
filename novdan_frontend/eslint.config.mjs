import withNuxt from "./.nuxt/eslint.config.mjs";
import js from "@eslint/js";
import pluginPrettierRecommended from "eslint-plugin-prettier/recommended";

export default withNuxt(
  js.configs.recommended,
  {
    rules: {
      "no-console": "warn",
      "no-alert": "warn",
    },
  },
  pluginPrettierRecommended,
);
