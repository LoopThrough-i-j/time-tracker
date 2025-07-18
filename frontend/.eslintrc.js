module.exports = {
	env: {
		browser: true,
		es2021: true,
		node: true,
	},
	extends: [
		"eslint:recommended",
		"plugin:react/recommended",
		"plugin:react-hooks/recommended",
	],
	parserOptions: {
		ecmaFeatures: {
			jsx: true,
		},
		ecmaVersion: "latest",
		sourceType: "module",
	},
	plugins: ["react", "react-hooks"],
	rules: {
		"react/react-in-jsx-scope": "off",
		"react/prop-types": "off",
		"no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
		"no-console": ["warn", { allow: ["warn", "error"] }],
		"react-hooks/rules-of-hooks": "error",
		"react-hooks/exhaustive-deps": "warn",
		"lines-between-class-members": ["error", "always"],
		"padding-line-between-statements": [
			"error",
			{ blankLine: "always", prev: "*", next: "return" },
			{ blankLine: "always", prev: "directive", next: "*" },
			{ blankLine: "any", prev: "directive", next: "directive" },
			{ blankLine: "always", prev: ["const", "let", "var"], next: "*" },
			{
				blankLine: "any",
				prev: ["const", "let", "var"],
				next: ["const", "let", "var"],
			},
			{ blankLine: "always", prev: "block-like", next: "*" },
			{ blankLine: "always", prev: "*", next: "block-like" },
			{ blankLine: "always", prev: "function", next: "*" },
			{ blankLine: "always", prev: "*", next: "function" },
			{ blankLine: "always", prev: "*", next: "if" },
			{ blankLine: "always", prev: "*", next: "for" },
			{ blankLine: "always", prev: "*", next: "while" },
			{ blankLine: "always", prev: "*", next: "try" },
			{ blankLine: "always", prev: "*", next: "switch" },
		],
		"lines-around-directive": ["error", "always"],
		"no-multiple-empty-lines": ["error", { max: 2, maxEOF: 1 }],
		"eol-last": ["error", "always"],
		indent: ["error", 2],
		quotes: ["error", "single"],
		semi: ["error", "always"],
		"comma-dangle": ["error", "always-multiline"],
		"object-curly-spacing": ["error", "always"],
		"array-bracket-spacing": ["error", "never"],
		"space-before-function-paren": [
			"error",
			{ anonymous: "always", named: "never", asyncArrow: "always" },
		],
		"keyword-spacing": ["error", { before: true, after: true }],
		"space-infix-ops": "error",
		"no-trailing-spaces": "error",
	},
	settings: {
		react: {
			version: "detect",
		},
	},
};
