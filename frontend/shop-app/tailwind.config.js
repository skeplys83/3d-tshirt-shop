export default {
  content: [
    './src/**/*.{html,js,svelte,ts}',
  ],
  theme: {
    extend: {
      colors: {
        white: '#ffffff',
        lightGrey: '#393939',
        blue: {
          DEFAULT: '#b6d0e2',
          hover: '#a7c7e0',
          dark: '#192E47',
        },
        grey: {
          DEFAULT: '#d3d3d3',
          menubar: '#f4f4f4',
          description: '#EDEDED',
          header: '#D9D9D9',
        },
        font: '#192e47',
        green: {
          DEFAULT: '#c1e2b6',
          hover: '#afdea0',
          status: '#aaff76',
        },
        yellow: {
          DEFAULT: '#edead4',
          hover: '#ece5bb',
          status: '#ffcc69',
        },
        red: {
          DEFAULT: '#e2bbb6',
          hover: '#e0ada7',
          status: '#ff7d7d',
        },
      },
      fontSize: {
        '2xl': '24px',
        'xl': '20px',
        'l': '16px',
        'm': '14px',
        's': '12px',
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
      borderWidth: {
        '1': '1px',
      },
      boxShadow: {
        't-sm': '0 -1px 2px 0 rgba(0, 0, 0, 0.05)',
        't-md': '0 -4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        't-lg': '0 -10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        't-xl': '0 -20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        't-2xl': '0 -25px 50px -12px rgba(0, 0, 0, 0.25)',
        't-3xl': '0 -35px 60px -15px rgba(0, 0, 0, 0.3)'
      },
      height: {
        '150': '35rem',
      },
      screens: {
        'xs': '360px',
      },
    },
  },
  plugins: [],
}