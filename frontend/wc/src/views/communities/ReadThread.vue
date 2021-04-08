<template>
  <div
    v-if="initialized"
  >

    <v-container
      class="pa-0"
    >
      <v-btn
        color="secondary"
        class="mr-2"
        @click="back()"
      >
        <v-icon
          class="mr-1"
        >
          mdi-keyboard-backspace
        </v-icon>
        {{ $t('common.BACK') }}
      </v-btn>

      <span
        v-if="hasPermission"
      >
        <v-btn
          fab
          small
          color="primary"
          class="mr-2"
        >
          <v-icon>mdi-square-edit-outline</v-icon>
        </v-btn>
        <v-btn
          fab
          small
          color="error"
          class="mr-2"
        >
          <v-icon>mdi-trash-can-outline</v-icon>
        </v-btn>
      </span>
      <span
        v-if="user.is_staff"
      >
        <v-btn
          fab
          small
          color="blue-grey lighten-4"
        >
          <v-icon>mdi-pin-outline</v-icon>
        </v-btn>
      </span>
    </v-container>

    <v-sheet
      color="grey lighten-4"
      class="my-3 pa-3 headline text-center"
    >
      {{ thread.title }}
    </v-sheet>

    <v-container
      class="pa-0"
    >
      <div
        class="mr-1 mb-4 text-right font-italic"
      >
        {{ getUsername(thread) }},
        {{ formatDateTime(thread.modified_at) }}
      </div>

      <v-sheet
        class="mb-5 pa-1 thread-content"
        v-html="thread.content"
      ></v-sheet>
    </v-container>

  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import FormatDate from '@/mixins/formatDate'
import Mobile from '@/mixins/mobile'

export default {
  mixins: [
    FormatDate,
    Mobile
  ],
  data () {
    return {
      thread: null,
      page: 1,
      forumName: null,
      firstInit: false,
    }
  },
  computed: {
    ...mapState([
      'user'
    ]),
    hasPermission () {
      if (this.user.is_staff) {
        return true
      }
      if (!this.user || !this.thread.user) {
        return false
      }
      return (this.user.id == this.thread.user.id)
    },
    initialized () {
      return this.firstInit
    },
  },
  metaInfo () {
    var title = this.$t('info.SITENAME')
    if (this.thread) {
      title = this.thread.title + ' | ' + this.$t('info.SITENAME')
    }
    return {
      title: title
    }
  },
  mounted () {
    this.getThread(this.$route.params.pk)
  },
  methods: {
    getThread: function (pk) {
      var vm = this
      this.page = this.$route.params.page
      this.forumName = this.$route.params.forum

      axios({
        method: this.$api('THREAD_RETRIEVE').method,
        url: this.$api('THREAD_RETRIEVE').url.replace(
          '{forum}', this.forumName).replace('{pk}', pk)
      })
      .then(function (response) {
        vm.thread = response.data['data']
        vm.firstInit = true
      })
    },
    getUsername: function (thread) {
      if (thread.user) {
        return thread.user.call_name
      }
      else {
        return thread.name
      }
    },
    back: function () {
      this.$router.push({
        name: 'communities.threadPage',
        params: {
          forum: this.$route.params.forum,
          page: this.$route.params.page
        },
        query: {
          q: this.$route.query.q
        }
      })
    }
  }
}
</script>

<style lang="scss">
  .thread-content {
    font-size: 18px;
    white-space: break-spaces;
  }
</style>
