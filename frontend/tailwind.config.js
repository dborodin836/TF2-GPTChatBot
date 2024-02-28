const withMT = require("@material-tailwind/react/utils/withMT");

module.exports = withMT({
  content: [
      "./src/**/*.{js,jsx,ts,tsx}",
      "node_modules/@material-tailwind/react/components/**/*.{js,ts,jsx,tsx}",
      "node_modules/@material-tailwind/react/theme/components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
});
