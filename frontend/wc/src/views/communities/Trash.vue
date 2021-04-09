<template>
  <v-container
    class="py-0"
  >
    <div
      v-if="initialized"
      class="content pa-0"
    >

      <div
        class="headline cursor-pointer"
        @click="resetTrash()"
      >
        {{ $t('forum.THREAD_TRASH') }}
      </div>
      <v-sheet
        class="mb-3 pa-2 body-2"
        v-text="forum.title"
        v-if="forum.title"
      ></v-sheet>

      <v-btn
        color="secondary"
        class="ml-2 mb-5"
        @click="$router.push({
          name: 'communities.thread',
          params: {
            forum: $route.params.forum
          }
        })"
      >
        <v-icon
          class="mr-1"
        >
          mdi-keyboard-backspace
        </v-icon>
        {{ $t('common.BACK') }}
      </v-btn>

      <v-dialog
        v-model="contentDialog"
        transition="dialog-bottom-transition"
        width="90%"
        :max-width="800"
      >
        <template v-slot:activator="{ on, attrs }">

          <v-simple-table>
            <tbody>
              <tr
                v-for="thread in threads"
                :key="thread.id"
              >
                <td
                  width="80"
                  class="body-2"
                  v-if="!isMobile"
                >
                  {{ thread.id }}
                </td>
                <td
                  class="pt-1 body-1"
                  v-bind="attrs"
                  v-on="on"
                  @click="initializeContentDialog(thread)"
                >
                  {{ thread.title }}
                  <div
                    v-if="isMobile"
                    class="caption blue-grey--text text-right"
                  >
                    <span>
                      {{ getUsername(thread) }}
                    </span>
                    <span>|</span>
                    <span>
                      {{ formatDateTime(thread.modified_at) }}
                    </span>
                  </div>
                </td>
                <td
                  width="120"
                  class="body-2"
                  v-if="!isMobile"
                >
                  {{ getUsername(thread) }}
                </td>
                <td
                  width="180"
                  class="body-2"
                  v-if="!isMobile"
                >
                  {{ formatDateTime(thread.modified_at) }}
                </td>
                <td
                  width="40"
                >
                  <v-btn
                    small
                    color="primary"
                    @click="restoreThread(thread)"
                  >
                    {{ $t('common.RESTORE' )}}
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-simple-table>

        </template>
        <v-card
          v-if="thread"
        >
          <v-card-title>
            {{ thread.title }}
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text
            v-html="thread.content"
            class="pa-5"
          >
          </v-card-text>
        </v-card>
      </v-dialog>

      <Pagination
        :pagination="pagination"
        :first="getTrash"
        :prev="getTrash"
        :next="getTrash"
        class="mt-5"
      />

    </div>
  </v-container>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
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
  data () {
    return {
      pagination: {
        pageTotal: 1,
        currentPage: 1,
        firstLink: null,
        prevLink: null,
        nextLink: null,
      },
      forum: null,
      threads: null,
      contentDialog: false,
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
    },
  },
  metaInfo () {
    return {
      title: this.$t('forum.THREAD_TRASH') + ' | ' + this.$t('info.SITENAME')
    }
  },
  mounted () {
    this.getTrash(null, this.$route.query.q)
  },
  methods: {
    getTrash: function (url=null, q='') {
      var vm = this
      var forumName = this.$route.params.forum

      if (!url) {
        url = this.$api('THREAD_TRASH').url.replace(
          '{forum}', forumName) + q
      }

      axios({
        method: this.$api('THREAD_TRASH').method,
        url: url
      })
      .then(function (response) {
        var pagination = response.data['pagination']
        vm.pagination.pageTotal = pagination['page_total']
        vm.pagination.currentPage = pagination['current_page']
        vm.pagination.prevLink = pagination['prev_link']
        vm.pagination.nextLink = pagination['next_link']
        vm.pagination.firstLink = pagination['first_link']

        vm.forum = response.data['data']['forum']
        vm.threads = response.data['data']['threads']
        vm.firstInit = true
      })
    },
    resetTrash: function () {
      this.$route.params.page = 1
      this.$root.$refs.Navigation.resetSearch()
      this.getTrash()
    },
    getUsername: function (thread) {
      if (thread.user) {
        return thread.user.call_name
      }
      else {
        return thread.name
      }
    },
    restoreThread: function (thread) {
      var vm = this
      var forumName = this.$route.params.forum

      axios({
        method: this.$api('THREAD_RESTORE').method,
        url: this.$api('THREAD_RESTORE').url.replace(
          '{forum}', forumName).replace('{pk}', thread.id)
      })
      .then(function () {
        var index = vm.threads.indexOf(thread)
        vm.threads.splice(index, 1)

        vm.$dialog.notify.success(
          vm.$t('forum.THREAD_RESTORED'), {
            position: 'bottom-right',
            timeout: 2000
          }
        )
      })
    },
    initializeContentDialog: function (thread) {
      this.thread = thread
    }
  }
}
</script>
