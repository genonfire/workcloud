<template>
  <div
    class="content text-center"
    v-if="user"
  >
    <v-form v-model="validation">
      <v-row justify="space-around">
        <v-col md=6>
          <v-sheet
            color="#eee"
            elevation="3"
            class="pa-5"
          >
            {{ $t('accounts.DEACTIVATE_DESCRIPTION') }}
          </v-sheet>
        </v-col>
      </v-row>

      <v-row justify="center">
        <v-col md="6">
          <v-checkbox
            v-model="consent"
            :rules="[v => !!v || $t('accounts.CONSENT_HINT')]"
            :label="$t('accounts.CONSENT')"
            required
          ></v-checkbox>
        </v-col>
      </v-row>

      <v-btn
        large
        color="error"
        @click="submit"
      >
        {{ $t('accounts.DEACTIVATE') }}
      </v-btn>
    </v-form>
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
      validation: false,
      consent: false,
    }
  },
  computed: {
    ...mapState([
      'user'
    ])
  },
  methods: {
    submit: async function () {
      if (!this.validation) {
        this.$dialog.notify.info(
          this.$t('accounts.CONSENT_HINT'), {
            position: 'top-right'
          }
        )
        return
      }

      let res = await this.$dialog.warning({
        text: this.$t('accounts.DEACTIVATE_ACCOUNT'),
        actions: {
          false: this.$t('common.CANCEL'),
          true: {
            color: 'error',
            text: this.$t('accounts.DEACTIVATE')
          }
        }
      })
      if (!res) {
        return
      }

      var vm = this

      axios({
        method: this.$api('ACCOUNTS_DEACTIVATE').method,
        url: this.$api('ACCOUNTS_DEACTIVATE').url,
        data: {
          consent: this.consent
        }
      })
      .then(function () {
        vm.$store.commit({
          type: 'removeUser'
        })

        localStorage.clear()

        axios.defaults.headers.common['Authorization'] = ''
        router.push({ name: 'home' })
      })
      .catch(function () {
      })
    },
  }
}
</script>
