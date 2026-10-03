module.exports = {
  content: ['./*.html', './assets/*.js'],
  theme: {
    extend: {
      colors: {
        brand: { 50: '#f5f7fa', 100: '#eaeef4', 400: '#64748b', 900: '#0f2d83' },
        accent: '#3454c4',
      },
      fontFamily: {
        display: ['"Big Shoulders Display"', 'sans-serif'],
        body: ['"IBM Plex Sans"', 'sans-serif'],
      },
    },
  },
}
