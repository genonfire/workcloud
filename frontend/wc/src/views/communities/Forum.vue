<template>
  <v-container>
    <div
      v-if="initialized"
      class="content pa-0"
    >
      <v-dialog
        v-model="editDialog"
        fullscreen
        transition="dialog-bottom-transition"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            color="primary"
            class="mb-5"
            v-bind="attrs"
            v-on="on"
            @click="newForum()"
          >
            <v-icon
              class="mr-2"
            >
              mdi-plus
            </v-icon>
            {{ $t('forum.NEW_FORUM') }}
          </v-btn>
          <v-simple-table>
            <thead>
              <th>{{ $t('forum.FORUM_ID') }}</th>
              <th>{{ $t('forum.FORUM_NAME') }}</th>
              <th
                v-if="!isMobile"
              >
                {{ $t('forum.THREAD_COUNT') }}
              </th>
              <th
                v-if="!isMobile"
              >
                {{ $t('forum.REPLY_COUNT') }}
              </th>
              <th>{{ $t('forum.ACTIVE') }}</th>
              <th>{{ $t('forum.MANAGE_FORUM') }}</th>
            </thead>
            <tbody>
              <tr
                v-for="forum in forums"
                :key="forum.id"
                class="pa-0 text-center"
                @click="openThread(forum)"
              >
                <td>{{ forum.id }}</td>
                <td>{{ forum.name }}</td>
                <td
                  v-if="!isMobile"
                >
                  {{ forum.thread_count }}
                </td>
                <td
                  v-if="!isMobile"
                >
                  {{ forum.reply_count }}
                </td>
                <td>
                  <v-icon
                    v-if="forum.option.is_active"
                    color="success"
                  >
                    mdi-check
                  </v-icon>
                </td>
                <td>
                  <v-btn
                    small
                    color="primary"
                    v-bind="attrs"
                    v-on="on"
                    @click="editForum(forum)"
                  >
                    {{ $t('forum.FORUM_EDIT') }}
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-simple-table>
        </template>

        <v-card
          v-if="editInitialized || editForNew"
        >
          <v-toolbar
            dark
            color="primary"
          >
            <v-btn
              icon
              dark
              @click="closeEditForum()"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-toolbar-title>{{ $t('forum.FORUM_EDIT') }}</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-toolbar-items>
              <v-btn
                dark
                text
                @click="saveForum()"
              >
                {{ $t('common.SAVE') }}
              </v-btn>
            </v-toolbar-items>
          </v-toolbar>

          <v-container>
            <v-list
              subheader
            >
              <v-subheader>{{ $t('common.GENERAL') }}</v-subheader>
              <v-list-item>
                <v-list-item-content>
                  <v-text-field
                    v-model="forum.name"
                    :rules="[rules.required, rules.alphanumberonly]"
                    :label="$t('forum.FORUM_NAME')"
                    :readonly="!editForNew"
                  ></v-text-field>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-text-field
                    v-model="forum.title"
                    :label="$t('forum.FORUM_TITLE')"
                  ></v-text-field>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-textarea
                    v-model="forum.description"
                    :label="$t('forum.FORUM_DESCRIPTION')"
                    background-color="grey lighten-5"
                    auto-grow
                    outlined
                  ></v-textarea>
                </v-list-item-content>
              </v-list-item>
            </v-list>
            <v-divider></v-divider>

            <v-list
              subheader
            >
              <v-subheader>{{ $t('forum.OPTION') }}</v-subheader>
              <v-list-item>
                <v-list-item-content>
                  <v-switch
                    v-model="forum.option.is_active"
                    :label="getActiveText"
                    inset
                    class="ml-3"
                  >
                  </v-switch>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-select
                    v-model="forum.option.permission_read"
                    :items="permissions"
                    :label="$t('forum.PERMISSION_READ')"
                    filled
                    outlined
                  >
                  </v-select>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-select
                    v-model="forum.option.permission_write"
                    :items="permissions"
                    :label="$t('forum.PERMISSION_WRITE')"
                    filled
                    outlined
                  >
                  </v-select>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-select
                    v-model="forum.option.permission_reply"
                    :items="permissions"
                    :label="$t('forum.PERMISSION_REPLY')"
                    filled
                    outlined
                  >
                  </v-select>
                </v-list-item-content>
              </v-list-item>
            </v-list>
            <v-divider></v-divider>

            <v-list
              subheader
            >
              <v-subheader>{{ $t('forum.MANAGERS') }}</v-subheader>
              <v-list-item>
                <v-list-item-content>
                  <v-combobox
                    v-model="managers"
                    :label="$t('forum.MANAGERS')"
                    :items="managerList"
                    multiple
                  >
                  </v-combobox>
                </v-list-item-content>
              </v-list-item>

              <v-list-item
                two-line
                v-if="!editForNew"
              >
                <v-list-item-content>
                  <v-alert
                    outlined
                    type="error"
                  >
                    <v-list-item-title>
                      {{ $t('forum.DELETE_FORUM') }}
                    </v-list-item-title>
                    <v-list-item-subtitle
                      class="danger_zone"
                    >
                      {{ $t('forum.DELETE_FORUM_DESCRIPTION') }}
                    </v-list-item-subtitle>
                    <div
                      class="float-right"
                      style="position:relative;"
                    >
                      <v-btn
                        color="error"
                        @click="deleteForum(forum)"
                      >
                        {{ $t('forum.DELETE_FORUM') }}
                      </v-btn>
                    </div>
                  </v-alert>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-container>
        </v-card>

      </v-dialog>

      <Pagination
        :pagination="pagination"
        :first="getForums"
        :prev="getForums"
        :next="getForums"
      />

    </div>
  </v-container>
</template>

<script>
import axios from 'axios'
import Pagination from '@/components/Pagination'
import Mobile from '@/mixins/mobile'
import { mapState } from 'vuex'

export default {
  mixins: [
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
        nextLink: null
      },
      permissions: [
        'all',
        'staff',
        'member'
      ],
      forums: null,
      forum: null,
      editDialog: false,
      forumRetrieved: false,
      editForNew: false,
      managers: [],
      managerList: [],
      firstInit: false,
      rules: {
        required: v => !!v || this.$t('common.REQUIRED'),
        alphanumberonly: v => /^[A-Za-z0-9]+$/.test(v) || this.$t('common.ALPHA_NUMBER_ONLY')
      },
    }
  },
  computed: {
    ...mapState([
      'user'
    ]),
    initialized () {
      return this.firstInit
    },
    editInitialized () {
      return this.forumRetrieved
    },
    getActiveText () {
      if (this.forum.option.is_active) {
        return this.$t('forum.ACTIVE')
      }
      else {
        return this.$t('forum.INACTIVE')
      }
    }
  },
  mounted () {
    this.getForums(null, this.$route.query.q)
    this.getManagers()
  },
  methods: {
    getForums: function (url=null, q='') {
      var vm = this

      if (!url) {
        url = this.$api('FORUM_LIST').url + q
      }

      axios({
        method: this.$api('FORUM_LIST').method,
        url: url
      })
      .then(function (response) {
        var pagination = response.data['pagination']
        vm.pagination.pageTotal = pagination['page_total']
        vm.pagination.currentPage = pagination['current_page']
        vm.pagination.prevLink = pagination['prev_link']
        vm.pagination.nextLink = pagination['next_link']
        vm.pagination.firstLink = pagination['first_link']

        vm.forums = response.data['data']
        vm.firstInit = true
      })
    },
    newForum: function () {
      this.forum = {
        'name': '',
        'title': '',
        'description': '',
        'option': {
          'is_active': true,
          'permission_read': 'member',
          'permission_write': 'member',
          'permission_reply': 'member'
        }
      }
      this.managers = [
        {
          'value': this.user.id,
          'text': this.user.username
        }
      ]
      this.editForNew = true
    },
    editForum: function (forum) {
      var vm = this

      axios({
        method: this.$api('FORUM_RETRIEVE').method,
        url: this.$api('FORUM_RETRIEVE').url.replace(
          '{pk}', forum.id
        )
      })
      .then(function (response) {
        vm.forum = response.data['data']
        vm.managers = vm.managerToItem(response.data['data']['managers'])
        vm.forumRetrieved = true
      })
    },
    closeEditForum: function () {
      this.forumRetrieved = false
      this.editForNew = false
      this.editDialog = false
    },
    saveForum: function () {
      var vm = this

      if (this.managers) {
        this.forum.managers = this.itemToManager(this.managers)
      }

      var method = this.$api('FORUM_CREATE').method
      var url = this.$api('FORUM_CREATE').url

      if (!this.editForNew) {
        method = this.$api('FORUM_EDIT').method
        url = this.$api('FORUM_EDIT').url.replace('{pk}', this.forum.id)
      }

      axios({
        method: method,
        url: url,
        data: this.forum
      })
      .then(function (response) {
        var forum = response.data['data']
        if (vm.editForNew) {
          vm.forums.unshift(forum)
        }
        else {
          for (var i=0; i<vm.forums.length; i++) {
            if (vm.forums[i].id == forum.id) {
              vm.forums[i].option.is_active = forum.option.is_active
              break
            }
          }
        }
        vm.closeEditForum()
      })
      .catch(function (error) {
        if (error.response && error.response.data) {
          for (var field in error.response.data) {
            vm.$dialog.notify.info(
              field + ': ' + error.response.data[field], {
                position: 'bottom-right'
              }
            )
          }
        }
      })
    },
    deleteForum: async function (forum) {
      let res = await this.$dialog.warning({
        text: this.$t('forum.DELETE_FORUM_DESCRIPTION'),
        actions: {
          false: this.$t('common.CANCEL'),
          true: {
            color: 'error',
            text: this.$t('forum.DELETE_FORUM')
          }
        }
      })

      if (res) {
        var vm = this

        axios({
          method: this.$api('FORUM_DELETE').method,
          url: this.$api('FORUM_DELETE').url.replace('{pk}', forum.id)
        })
        .then(function () {
          var index = vm.forums.indexOf(forum)
          vm.forums.splice(index, 1)
          vm.closeEditForum()
        })
      }
    },
    getManagers: async function () {
      var vm = this

      axios({
        method: this.$api('ACCOUNTS_STAFF_SEARCH').method,
        url: this.$api('ACCOUNTS_STAFF_SEARCH').url
      })
      .then(function (response) {
        vm.managerList = vm.managerToItem(response.data['data'])
      })
    },
    managerToItem: function (managers) {
      var managerList = []

      for (var i=0; i<managers.length; i++) {
        var item = {
          'value': managers[i]['id'],
          'text': managers[i]['username']
        }
        managerList.push(item)
      }
      return managerList
    },
    itemToManager: function (items) {
      var managers = []

      for (var i=0; i<items.length; i++) {
        var manager = {
          'id': items[i].value
        }
        managers.push(manager)
      }
      return managers
    },
    openThread: function (forum) {
      this.$router.push({
        name: 'communities.thread',
        params: {
          forum: forum.name
        }
      })
    }
  }
}
</script>

<style lang="scss">
.danger_zone {
  white-space: break-spaces;
}
</style>
