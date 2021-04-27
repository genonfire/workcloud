<template>
  <v-container>

    <v-navigation-drawer
      v-model="drawer"
      app
    >
      <template>
        <v-list-item
          one-line
          v-if="user"
        >
          <v-list-item-avatar>
            <v-img
              :src="user.photo"
              v-if="user.photo"
            ></v-img>
            <v-icon
              v-else
            >
              mdi-account
            </v-icon>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title>{{ call_name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item
          v-else
        >
          <v-list-item-avatar>
            <v-icon>mdi-account</v-icon>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title>
              <router-link :to="{ name: 'accounts.login' }">
                {{ $t('accounts.LOGIN') }}
              </router-link>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list
          nav
          dense
        >
          <v-list-item-group>
            <v-list-item
              v-for="(m, i) in menu"
              :key="i"
            >
              <v-list-item-icon>
                <v-icon v-text="m.icon"></v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <router-link :to="m.to">
                  <v-list-item-title v-text="m.text"></v-list-item-title>
                </router-link>
              </v-list-item-content>
            </v-list-item>

          </v-list-item-group>
        </v-list>

      </template>
    </v-navigation-drawer>

    <v-app-bar
      class="nav"
      app
    >
      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
      >
      </v-app-bar-nav-icon>

      <router-link :to="{ name: 'home' }">
        <v-img
          src="@/assets/images/logo.png"
          max-width="50"
        ></v-img>
      </router-link>

      <v-spacer></v-spacer>

      <v-text-field
        id="search"
        ref="search"
        v-model="search"
        outlined
        dense
        single-line
        clearable
        hide-details
        prepend-inner-icon="mdi-magnify"
        :placeholder="$t('common.SEARCH')"
        @blur="onBlur"
        @keydown.esc="onEsc"
        @keydown.enter="onEnter"
        accesskey="/"
      >
      </v-text-field>

    </v-app-bar>

  </v-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Navigation',
  data () {
    return {
      drawer: null,
      search: '',
    }
  },
  computed: {
    ...mapState([
      'user'
    ]),
    call_name: function () {
      if (this.user.call_name)
        return this.user.call_name
      else
        return this.user.username
    },
    menu: function () {
      var menuList = []

      if (this.user.is_staff) {
        menuList.push(
          {
            text: this.$t('common.DASHBOARD'),
            icon: 'mdi-monitor-dashboard',
            to: { name: 'manage' }
          }
        )
      }

      if (this.user) {
        menuList.push(
          {
            text: this.$t('accounts.SETTING'),
            icon: 'mdi-cog',
            to: { name: 'accounts.profile' }
          },
          {
            text: this.$t('accounts.LOGOUT'),
            icon: 'mdi-logout',
            to: { name: 'accounts.logout' }
          }
        )
      }
      return menuList
    }
  },
  created () {
    this.$root.$refs.Navigation = this
  },
  beforeDestroy () {
    document.onkeydown = null
  },
  methods: {
    onBlur () {
    },
    onEsc () {
      this.$refs.search.blur()
    },
    resetSearch () {
      this.$nextTick(() => (this.search = undefined))
    },
    onEnter () {
      this.searchAnything(this.search)
    },
    searchAnything(anything) {
      this.onEsc()

      var route_name = this.$route.name
      if (!(this.$route.name in this.$const('SEARCH_ROUTES'))) {
        this.resetSearch()
        return
      }

      this.$router.push({
        name: 'search',
        params: {
          name: route_name,
          forum: this.$route.params.forum,
          q: anything
        }
      })
    }
  }
}
</script>

<style lang="scss">
.nav {
  a {
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
.v-list-item {
  min-height:30px;

  a {
    color: rgba(0, 0, 0, 0.88) !important;
    text-decoration: none;
  }
  a:hover {
    color: #c0341d !important;
    text-decoration: underline;
  }
}
</style>
