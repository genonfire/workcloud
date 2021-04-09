<template>
  <div
    class="content text-center"
  >
    <v-row justify="space-around">
      <v-col md=6>
        <v-sheet
          color="#eee"
          elevation="3"
          class="mb-5 pa-5"
        >
        {{ $t('accounts.PASSWORD_RESET_CONFIRM') }}
        </v-sheet>
      </v-col>
    </v-row>

    <v-form
        v-model="validation"
      >

      <v-row justify="center">
        <v-col cols="12" md="3">
          <v-text-field
            v-model="password1"
            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required, rules.min]"
            :type="show1 ? 'text' : 'password'"
            name="password1"
            :label="$t('accounts.PASSWORD')"
            :hint="$t('common.REQUIRED_MIN', { min: $const('PASSWORD_MIN') })"
            counter
            @click:append="show1 = !show1"
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            v-model="password2"
            :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required, rules.passwordMatch]"
            :type="show2 ? 'text' : 'password'"
            name="password2"
            :label="$t('accounts.PASSWORD_CONFIRM')"
            counter
            @click:append="show2 = !show2"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-btn
        color="primary"
        class="mt-6"
        @click="submit"
      >
        {{ $t('common.SUBMIT') }}
      </v-btn>

    </v-form>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      validation: false,
      password1: '',
      password2: '',
      show1: false,
      show2: false,
      rules: {
        required: v => !!v || this.$t('common.REQUIRED'),
        min: v => v.length >= this.$const('PASSWORD_MIN') || this.$t('common.REQUIRED_MIN', { min: this.$const('PASSWORD_MIN') }),
        passwordMatch: () => this.password1 === this.password2 || this.$t('accounts.PASSWORD_NOT_MATCH'),
      },
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
        method: this.$api('ACCOUNTS_PASSWORD_RESET_CONFIRM').method,
        url: this.$api('ACCOUNTS_PASSWORD_RESET_CONFIRM').url,
        data: {
          new_password: this.password1,
          uid: this.$route.params.uid,
          token: this.$route.params.token
        },
      })
      .then(function () {
        vm.$store.commit({
          type: 'removeUser'
        })

        localStorage.clear()
        axios.defaults.headers.common['Authorization'] = ''

        vm.$router.push({ name: 'accounts.login' })
        vm.$dialog.notify.success(
          vm.$t('accounts.PASSWORD_RESET_COMPLETED'), {
            position: 'bottom-right'
          }
        )
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
