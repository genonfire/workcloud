<template>
  <div class="content">
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data () {
    return {
    }
  },
  computed: {
    ...mapState([
      'user'
    ])
  },
  mounted () {
    if (this.user) {
      this.$router.push({ name: 'home' })
    }
    else {
      this.$router.push({ name: 'accounts.login' })
    }
  }
}
</script>
