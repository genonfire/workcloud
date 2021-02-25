<template>
  <div class="content">
  </div>
</template>

<script>
import router from '@/router'
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
      router.push({ name: 'home' })
    }
    else {
      router.push({ name: 'accounts.login' })
    }
  }
}
</script>
