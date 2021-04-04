<template>
  <div
    class="content text-center"
  >
    <v-progress-circular
      :size="70"
      :width="7"
      indeterminate
      color="#4CAF50"
    ></v-progress-circular>
  </div>
</template>

<script>
export default {
  data () {
    return {
      routerList: {
        // router name from: router name to
        'communities.forum': 'communities.forum'
      }
    }
  },
  mounted () {
    this.$router.replace({
      name: this.routerList[this.$route.params.name],
      query: {
        q: this.$route.params.q
      }
    })
  }
}
</script>
