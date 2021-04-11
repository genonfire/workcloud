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
        v-if="thread.has_permission"
      >
        <v-btn
          fab
          small
          color="primary"
          class="mr-2"
          @click="editThread(thread)"
        >
          <v-icon>mdi-square-edit-outline</v-icon>
        </v-btn>
        <v-btn
          fab
          small
          color="error"
          class="mr-2"
          @click="deleteThread(thread)"
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
          @click="pinThread(thread, thread.is_pinned)"
        >
          <v-icon
            v-if="thread.is_pinned"
          >
            mdi-pin-off-outline
          </v-icon>
          <v-icon
            v-else
          >
            mdi-pin-outline
          </v-icon>
        </v-btn>
      </span>
    </v-container>

    <v-sheet
      color="grey lighten-4"
      class="my-3 pa-3 headline text-center"
      :class="thread.is_pinned ? 'font-weight-bold' : ''"
    >
      <v-icon
        v-if="thread.is_pinned"
      >
        mdi-pin-outline
      </v-icon>
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

    <Reply
      :thread="thread"
    />

  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import FormatDate from '@/mixins/formatDate'
import Mobile from '@/mixins/mobile'
import Reply from './Reply'

export default {
  mixins: [
    FormatDate,
    Mobile
  ],
  components: {
    Reply
  },
  data () {
    return {
      page: 1,
      forumName: null,
      thread: null,
      firstInit: false,
    }
  },
  computed: {
    ...mapState([
      'user'
    ]),
    initialized () {
      return this.firstInit
    }
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
    getUsername: function (threadOrReply) {
      if (threadOrReply.user) {
        return threadOrReply.user.call_name
      }
      else {
        return threadOrReply.name
      }
    },
    editThread: function (thread) {
      this.$router.push({
        name: 'communities.editThread',
        params: {
          forum: this.$route.params.forum,
          page: this.$route.params.page,
          pk: thread.id
        },
        query: {
          q: this.$route.query.q
        }
      })
    },
    deleteThread: async function (thread) {
      var res = await this.$dialog.warning({
        text: this.$t("forum.DELETE_THREAD_QUESTION"),
        actions: {
          false: this.$t('common.CANCEL'),
          true: {
            color: 'error',
            text: this.$t('common.DELETE')
          }
        }
      })
      if (!res) {
        return
      }

      var vm = this

      axios({
        method: this.$api('THREAD_DELETE').method,
        url: this.$api('THREAD_DELETE').url.replace(
          '{forum}', this.forumName).replace('{pk}', thread.id)
      })
      .then(function () {
        vm.back()
        vm.$dialog.notify.success(
          vm.$t('common.DELETED'), {
            position: 'bottom-right',
            timeout: 2000
          }
        )
      })
    },
    pinThread: function (thread, unpin=false) {
      var vm = this
      var apiType = 'THREAD_PIN'

      if (unpin) {
        apiType = 'THREAD_UNPIN'
      }

      axios({
        method: this.$api(apiType).method,
        url: this.$api(apiType).url.replace(
          '{forum}', this.forumName).replace('{pk}', thread.id
        )
      })
      .then(function (response) {
        vm.thread = response.data['data']

        var pinText = 'forum.THREAD_PINNED'
        if (unpin) {
          pinText = 'forum.THREAD_UNPINNED'
        }

        vm.$dialog.notify.success(
          vm.$t(pinText), {
            position: 'bottom-right',
            timeout: 2000
          }
        )
      })
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
