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
          src="@/assets/logo.png"
          max-width="50"
        ></v-img>
      </router-link>

      <v-spacer></v-spacer>

      <v-responsive>
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
        >
        </v-text-field>
      </v-responsive>

    </v-app-bar>

  </v-container>
</template>

<style lang="scss">
.nav {
  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
.v-list-item {
  min-height:30px;

  a {
    font-size:0.9em !important;
    color: rgba(0, 0, 0, 0.88) !important;
    text-decoration: none;
  }
  a:hover {
    color: #c0341d !important;
    text-decoration: underline;
  }
}
</style>

<script>
  import { mapState } from 'vuex';

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
        if (this.user) {
          return [
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
          ]
        }
        else {
          return []
        }
      },
    },
    beforeDestroy () {
      document.onkeydown = null
    },
    methods: {
      onBlur () {
        this.resetSearch()
      },
      onEsc () {
        this.resetSearch()
        this.$refs.search.blur()
      },
      resetSearch () {
        this.$nextTick(() => (this.search = undefined))
      },
      onEnter () {
        this.searchAnything(this.search)
      },
      searchAnything(anything) {
        // TODO: implement search
        window.console.log(anything)
        this.onBlur()
      }
    }
  }
</script>
