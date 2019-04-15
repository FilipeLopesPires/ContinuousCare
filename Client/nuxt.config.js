import pkg from './package'

export default {
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
      { rel: 'icon', type: 'image/x-icon', href: '/logo.ico' }
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
    ]
  },

  /* Customize the progress-bar color */
  loading: { color: '#3ea8df', height: '4px', duration: 5000 },

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
    '~plugins/core-components.js',
    /* { src: '~/plugins/localStorage.js', ssr: false },
    { src: '~node_modules/vuex-persistedstate', ssr: false},
    { src: '~node_modules/vue-js-modal', ssr: false},
    { src: '~node_modules/apexcharts', ssr: false},
    { src: '~node_modules/vue-apexcharts', ssr: false}, */
  ],

  /* Nuxt.js modules */
  modules: [
    '@nuxtjs/axios',
    'bootstrap-vue/nuxt',
  ],
  /* Axios module configuration */
  axios: {
    baseURL: "http://mednat.ieeta.pt:8342",
  },

  env: {
    //baseURL: "http://192.168.43.136:5000",
  },

  /* Build configuration */
  build: {
    extend(config, ctx) {
    }
  }
}
