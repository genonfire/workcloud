<template>
  <div
    class="content text-center"
    v-if="user"
  >
    <v-row justify="space-around">
      <v-col md=6>
        <v-sheet
          color="#eee"
          elevation="3"
          class="mb-5 pa-5"
        >
          {{ $t('accounts.LOGOUT_DESCRIPTION') }}
        </v-sheet>
      </v-col>
    </v-row>
    <v-btn
      large
      color="primary"
      @click="logout"
    >
      {{ $t('accounts.LOGOUT') }}
    </v-btn>
  </div>

  <div
    class="content text-center"
    v-else
  >
    <v-row justify="space-around">
      <v-col md=6>
        <v-sheet
          color="#eee"
          elevation="3"
          class="mb-5 pa-5"
        >
          {{ $t('accounts.LOGIN_REQUIRED') }}
        </v-sheet>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios'
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
  methods: {
    logout: function () {
      var vm = this

      axios({
        method: this.$api('ACCOUNTS_LOGOUT').method,
        url: this.$api('ACCOUNTS_LOGOUT').url,
      })
      .then(function () {
        vm.$store.commit({
          type: 'removeUser'
        })

        localStorage.clear()

        axios.defaults.headers.common['Authorization'] = ''
        vm.$dialog.notify.success(
          vm.$t('accounts.LOGOUT_COMPLETED'), {
            position: 'top-right'
          }
        )
        router.push({ name: 'home' })
      })
      .catch(function () {
        router.push({ name: 'home' })
      })
    },
  }
}
</script>
