const pkg = require('./package')


module.exports = {
  mode: 'universal',

  /* Headers of the page */
  head: {
    title: pkg.name,
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: pkg.description }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ],
    script: [
      { src: '/js/jquery-3.2.1.min.js'},
      { src: '/js/bootstrap.min.js'},
      { src: '/js/popper.js'},
      { src: '/js/stellar.js'},
      { src: '/vendors/isotope/isotope-min.js'},
      { src: '/vendors/lightbox/simpleLightbox.min.js'},
      { src: '/vendors/isotope/imagesloaded.pkgd.min.js'},
      { src: '/vendors/jquery-ui/jquery-ui.js'},
      { src: '/vendors/nice-select/js/jquery.nice-select.min.js'},
      { src: 'https://cdnjs.cloudflare.com/ajax/libs/Counter-Up/1.0.0/jquery.counterup.min.js'},
      { src: 'https://cdnjs.cloudflare.com/ajax/libs/waypoints/4.0.1/jquery.waypoints.min.js'},
      { src: 'https://maps.googleapis.com/maps/api/js?key=AIzaSyA7nx22ZmINYk9TGiXDEXGVxghC43Ox6qA'}, // key problem must be solved
    ]
  },

  /* Customize the progress-bar color */
  loading: { color: '#fff' },

  /* Global CSS */
  css: [
    "~assets/css/bootstrap.css",
    "~assets/vendors/linericon/style.css",
    "~assets/css/font-awesome.min.css",
    "~assets/vendors/lightbox/simpleLightbox.css",
    "~assets/vendors/nice-select/css/nice-select.css",
    "~assets/vendors/animate-css/animate.css",
    "~assets/vendors/jquery-ui/jquery-ui.css",
    "~assets/css/style.css",
    "~assets/css/responsive.css"
  ],

  /* Plugins to load before mounting the App */
  plugins: [
    { src: '~plugins/js/mail-script.js', ssr: false},
    { src: '~plugins/js/custom.js', ssr: false},
    { src: '~plugins/js/jquery.ajaxchimp.min.js', ssr: false},
  ],

  /* Nuxt.js modules */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    // Doc: https://bootstrap-vue.js.org/docs/
    'bootstrap-vue/nuxt',
  ],

  /* Axios module configuration */
  axios: {
    // See https://github.com/nuxt-community/axios-module#options
  },

  /* Build configuration */
  build: {
    // You can extend webpack config here
    extend(config, ctx) {
      
    }
  }
}
