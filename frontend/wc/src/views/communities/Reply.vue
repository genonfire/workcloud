<template>
  <v-container
    class="pa-0"
  >
    <v-dialog
      v-model="replyDialog"
      persistent
      transition="dialog-bottom-transition"
      width="90%"
      :max-width="800"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-container
          class="pa-0"
        >

          <v-sheet
            class="my-2"
          >
            <v-btn
              small
              outlined
              class="mr-2 mb-1"
              :loading="replyLoading"
              :disabled="replyLoading"
              @click="getReplies(null)"
            >
              <v-icon>mdi-refresh</v-icon>
            </v-btn>

            {{ $t('forum.REPLY_COUNT') }} [{{ replyCount }}]
            <v-btn
              small
              outlined
              v-bind="attrs"
              v-on="on"
              class="mb-1 float-right"
              @click="initializeReplyDialog(
                getUsername(thread), thread.content, 0
              )"
              v-if="thread.forum.permission_reply && !reply.is_deleted"
            >
              <v-icon>mdi-reply-outline</v-icon>
              {{ $t('forum.REPLY') }}
            </v-btn>
          </v-sheet>

          <v-card
            v-for="reply in replies"
            :key="reply.id"
            outlined
            class="mb-1"
            :class="reply.reply_id ? 'ml-5': ''"
            :disabled="reply.is_deleted"
          >
            <v-card-text
              class="py-1 px-3"
              style="background-color: #ECEFF1"
            >
              <span
                class="mr-2 font-weight-bold"
              >
                {{ getUsername(reply) }}
              </span>
              <span
                class="text-caption"
              >
                {{ getDateOrTime(reply.date_or_time) }}
              </span>
              <v-btn
                small
                icon
                color="error"
                class="ml-1"
                @click="deleteReply(reply)"
                v-if="reply.has_permission && !reply.is_deleted"
              >
                <v-icon>mdi-alpha-x</v-icon>
              </v-btn>
              <v-btn
                icon
                v-bind="attrs"
                v-on="on"
                @click="initializeReplyDialog(
                  getUsername(reply), reply.content, reply.id
                )"
                v-if="thread.forum.permission_reply && !reply.is_deleted"
              >
                <v-icon>mdi-reply-outline</v-icon>
              </v-btn>
            </v-card-text>
            <v-card-text
              class="py-2 px-3 reply-content"
            >
              {{ reply.content }}
            </v-card-text>
          </v-card>
        </v-container>

      </template>
      <v-card
        v-if="replyDialog"
      >
        <v-card-title>
          {{ replyTo }}
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text
          class="py-2 px-3"
          v-html="replyToContent"
        >
        </v-card-text>
        <v-textarea
          v-model="replyContent"
          :label="$t('forum.REPLY_CONTENT')"
          background-color="grey lighten-5"
          auto-grow
          outlined
          autofocus
          class="mx-2 mt-2 mb-0"
        ></v-textarea>
        <v-card-actions
          class="pb-3"
        >
          <v-btn
            @click="replyDialog = !replyDialog"
          >
            {{ $t('common.CANCEL' )}}
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click="reply()"
          >
            {{ $t('forum.REPLY' )}}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <Pagination
      :pagination="pagination"
      :first="getReplies"
      :prev="getReplies"
      :next="getReplies"
      class="mt-5"
    />
  </v-container>
</template>

<script>
import axios from 'axios'
import Pagination from '@/components/Pagination'
import FormatDate from '@/mixins/formatDate'
import Mobile from '@/mixins/mobile'

export default {
  mixins: [
    FormatDate,
    Mobile
  ],
  components: {
    Pagination
  },
  props: {
    thread: Object
  },
  data () {
    return {
      pagination: {
        pageTotal: 1,
        currentPage: 1,
        firstLink: null,
        prevLink: null,
        nextLink: null,
      },
      replies: null,
      replyCount: 0,
      replyLoading: false,
      replyLoaded: false,
      replyDialog: false,
      replyContent: null,
      replyTo: null,
      replyToContent: null
    }
  },
  mounted () {
    this.getReplies(null)
  },
  methods: {
    getUsername: function (threadOrReply) {
      if (threadOrReply.user) {
        return threadOrReply.user.call_name
      }
      else {
        return threadOrReply.name
      }
    },
    getReplies: async function (url=null) {
      var vm = this
      var thread_id = this.thread.id
      this.replyLoading = true

      if (!url) {
        url = this.$api('THREAD_REPLIES').url.replace('{pk}', thread_id)
      }

      axios({
        method: this.$api('THREAD_REPLIES').method,
        url: url
      })
      .then(function (response) {
        var pagination = response.data['pagination']
        vm.pagination.pageTotal = pagination['page_total']
        vm.pagination.currentPage = pagination['current_page']
        vm.pagination.prevLink = pagination['prev_link']
        vm.pagination.nextLink = pagination['next_link']
        vm.pagination.firstLink = pagination['first_link']
        vm.replyCount = pagination['item_total']

        vm.replies = response.data['data']
        vm.replyLoading = false
        vm.replyLoaded = true
      })
    },
    reply: function () {
      var vm = this
      var thread_id = this.thread.id
      var content = this.replyContent
      var replyId = this.replyToId

      axios({
        method: this.$api('THREAD_REPLY').method,
        url: this.$api('THREAD_REPLY').url.replace('{pk}', thread_id),
        data: {
          reply_id: replyId,
          content: content
        }
      })
      .then(function () {
        vm.getReplies(null)
        vm.replyDialog = false
        vm.replyTo = null
        vm.replyToContent = null
        vm.replyContent = null
      })
      .catch(function (error) {
        if (error.response && error.response.data) {
          for (var field in error.response.data) {
            vm.$dialog.notify.info(
              field + ': ' + error.response.data[field], {
                position: 'top-right'
              }
            )
          }
        }
      })
    },
    initializeReplyDialog: function (replyTo, replyToContent, reply_id) {
      this.replyContent = null
      this.replyTo = replyTo
      this.replyToContent = replyToContent
      this.replyToId = reply_id
    },
    deleteReply: async function (reply) {
      var res = await this.$dialog.warning({
        text: this.$t("forum.DELETE_REPLY_QUESTION"),
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
        method: this.$api('REPLY_DELETE').method,
        url: this.$api('REPLY_DELETE').url.replace('{pk}', reply.id)
      })
      .then(function () {
        for (var i=0; i<vm.replies.length; i++) {
          if (vm.replies[i].id == reply.id) {
            vm.replies[i].is_deleted = true
            vm.replies[i].content = null
            break
          }
        }
      })
      .catch(function (error) {
        if (error.response && error.response.data) {
          for (var field in error.response.data) {
            vm.$dialog.notify.info(
              field + ': ' + error.response.data[field], {
                position: 'top-right'
              }
            )
          }
        }
      })
    }
  }
}
</script>

<style lang="scss">
.reply-content {
  white-space: break-spaces;
}
</style>
