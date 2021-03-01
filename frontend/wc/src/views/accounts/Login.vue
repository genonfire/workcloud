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
          {{ $t('accounts.ALREADY_LOGGEDIN') }}
        </v-sheet>
      </v-col>
    </v-row>
  </div>
  <div
    class="content text-center"
    v-else
  >
    <v-container>
      <v-form
        v-model="validation"
      >

        <v-row justify="center">
          <v-col
            cols="50"
            md="6"
          >
            <v-text-field
              v-model="username"
              :rules="[rules.required, rules.emailRules]"
              :label="$t('accounts.USERNAME')"
              :hint="$t('common.EMAIL_TYPE')"
            >
            </v-text-field>
          </v-col>
        </v-row>

        <v-row justify="center">
          <v-col cols="50" md="6">
            <v-text-field
              v-model="password"
              :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="[rules.required]"
              :type="show ? 'text' : 'password'"
              :label="$t('accounts.PASSWORD')"
              @click:append="show = !show"
              autocomplete
            ></v-text-field>
          </v-col>
        </v-row>

        <v-btn
          color="primary"
          class="mt-4 mb-10"
          @click="submit"
        >
          {{ $t('accounts.LOGIN') }}
        </v-btn>

        <v-row justify="space-around">
          <v-btn
            :to="{ name: 'accounts.signup' }"
          >
            {{ $t('accounts.SIGNUP') }}
          </v-btn>
          <v-btn
            :to="{ name: 'accounts.password_reset' }"
          >
            {{ $t('accounts.PASSWORD_RESET') }}
          </v-btn>
        </v-row>


      </v-form>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  data () {
    return {
      validation: false,
      username: '',
      password: '',
      show: false,
      rules: {
        required: v => !!v || this.$t('common.REQUIRED'),
        min: v => v.length >= 8 || this.$t('common.MIN_8'),
        emailRules: v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || this.$t('common.INVALID_EMAIL'),
      },
    }
  },
  computed: {
    ...mapState([
      'user'
    ])
  },
  mounted () {
    var nextURL = this.$route.query.nextURL
    if (this.$store.getters.isApproved && nextURL) {
      this.$router.replace({
        path: nextURL,
        params: this.$route.params
      })
    }
  },
  methods: {
    submit: function () {
      var vm = this

      if (!this.validation) {
        this.$dialog.notify.info(
          this.$t('common.INPUT_ERROR'), {
            position: 'top-right'
          }
        )
        return
      }

      axios({
        method: this.$api('ACCOUNTS_LOGIN').method,
        url: this.$api('ACCOUNTS_LOGIN').url,
        data: {
          username: this.username,
          password: this.password,
        },
      })
      .then(function (response) {
        var key = response.data['data']['key']
        var user = response.data['data']['user']
        var login_device = response.data['data']['login_device']

        vm.$store.commit({
          type: 'updateUser',
          key: key,
          user: user,
          login_device: login_device
        })

        axios.defaults.headers.common['Authorization'] = 'Token ' + key

        if (login_device.is_registered) {
          localStorage.setItem('token', key)
          vm.$router.push({ name: 'home' })
        }
        else {
          vm.$router.push({ name: 'accounts.register_device' })
        }
      })
      .catch(function (error) {
        if (error.response) {
          vm.$dialog.notify.warning(
            vm.$t('accounts.LOGIN_FAILED'), {
              position: 'top-right'
            }
          )
        }
        else {
          vm.$dialog.notify.error(
            vm.$t('error.LOGIN_LOGIC'), {
              position: 'top-right',
              timeout: 0
            }
          )
        }
      })
    }
  }
}
</script>
