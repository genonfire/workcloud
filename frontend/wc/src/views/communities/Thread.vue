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
        @click="resetThread()"
      >
        {{ forum.title }}
      </div>
      <v-sheet
        class="mb-3 pa-2 body-2"
        v-html="forum.description"
        v-if="forum.description"
      ></v-sheet>

      <v-btn
        color="primary"
        class="mb-5"
        @click="writeThread()"
        v-if="forum.permission_write"
      >
        <v-icon
          class="mr-2"
        >
          mdi-plus
        </v-icon>
        {{ $t('forum.WRITE_THREAD') }}
      </v-btn>
      <v-btn
        class="ml-2 mb-5"
        v-if="user.is_staff"
        @click="$router.push({
          name: 'communities.trash',
          params: {
            forum: $route.params.forum
          }
        })"
      >
        <v-icon>mdi-trash-can-outline</v-icon>
      </v-btn>

      <v-simple-table>
        <tbody>
          <tr
            v-for="thread in threads"
            :key="thread.id"
            class="cursor-pointer"
            @click="readThread(thread)"
          >
            <td
              class="pt-1 body-1"
              :class="thread.is_pinned ? 'font-weight-bold' : ''"
            >
              <v-icon
                dense
                color="blue-grey darken-2"
                v-if="thread.is_pinned"
              >
                mdi-pin-outline
              </v-icon>
              {{ thread.title }}
              <div
                v-if="isMobile"
                class="body-2 blue-grey--text text-right"
              >
                <span>
                  {{ getUsername(thread) }}
                </span>
                <span>|</span>
                <span>
                  {{ getDateOrTime(thread.date_or_time) }}
                </span>
              </div>
            </td>
            <td
              width="150"
              class="body-2"
              v-if="!isMobile"
            >
              {{ getUsername(thread) }}
            </td>
            <td
              width="120"
              class="body-2"
              v-if="!isMobile"
            >
              {{ getDateOrTime(thread.date_or_time) }}
            </td>
          </tr>
        </tbody>
      </v-simple-table>

      <Pagination
        :pagination="pagination"
        :first="firstPage"
        :prev="prevPage"
        :next="nextPage"
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
    var title = this.$t('info.SITENAME')
    if (this.forum) {
      title = this.forum.title + ' | ' + this.$t('info.SITENAME')
    }
    return {
      title: title
    }
  },
  mounted () {
    this.getThreads(null, this.$route.query.q)
  },
  methods: {
    firstPage: function (url) {
      this.$route.params.page = 1
      this.getThreads(url)
    },
    prevPage: function (url) {
      --this.$route.params.page
      this.getThreads(url)
    },
    nextPage: function (url) {
      ++this.$route.params.page
      this.getThreads(url)
    },
    getThreads: function (url=null, q='') {
      var vm = this
      var page = this.$route.params.page
      var forumName = this.$route.params.forum

      if (!url) {
        url = this.$api('THREAD_LIST').url.replace(
          '{forum}', forumName).replace('{page}', page) + q
      }

      axios({
        method: this.$api('THREAD_LIST').method,
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
    resetThread: function () {
      this.$route.params.page = 1
      this.$root.$refs.Navigation.resetSearch()
      this.getThreads()
    },
    getUsername: function (thread) {
      if (thread.user) {
        return thread.user.call_name
      }
      else {
        return thread.name
      }
    },
    readThread: function (thread) {
      this.$router.push({
        name: 'communities.readThread',
        params: {
          forum: this.$route.params.forum,
          page: this.$route.params.page,
          pk: thread.id,
          title: thread.title.replace(/\s+/g, '-')
        },
        query: {
          q: this.$route.query.q
        }
      })
    },
    writeThread: function () {
      this.$router.push({
        name: 'communities.writeThread',
        params: {
          forum: this.$route.params.forum,
          page: this.$route.params.page,
        },
        query: {
          q: this.$route.query.q
        }
      })
    }
  }
}
</script>
