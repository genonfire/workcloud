var Mobile = {
  data () {
    return {
      isMobile: false
    }
  },
  mounted () {
    this.onResize()
    window.addEventListener('resize', this.onResize, { passive: true })
  },
  methods: {
    onResize () {
      this.isMobile = window.innerWidth < 600
    }
  }
}

export default Mobile
