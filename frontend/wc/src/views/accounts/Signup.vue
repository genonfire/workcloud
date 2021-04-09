<template>
  <div class="content text-center">
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
              autocomplete
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
              autocomplete
            ></v-text-field>
          </v-col>
        </v-row>

        <v-row justify="center">
          <v-col
            cols="12"
            sm="3"
          >
            <v-text-field
              v-model="firstname"
              :counter="20"
              :rules="[rules.required]"
              :label="$t('accounts.FIRSTNAME')"
            ></v-text-field>
          </v-col>
          <v-col
            cols="12"
            md="3"
          >
            <v-text-field
              v-model="lastname"
              :counter="20"
              :rules="[rules.required]"
              :label="$t('accounts.LASTNAME')"
              required
            ></v-text-field>
          </v-col>
        </v-row>

        <v-btn
          color="primary"
          class="mt-6"
          @click="submit"
        >
          {{ $t('accounts.SIGNUP') }}
        </v-btn>

      </v-form>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      validation: false,
      username: '',
      password1: '',
      password2: '',
      firstname: '',
      lastname: '',
      show1: false,
      show2: false,
      rules: {
        required: v => !!v || this.$t('common.REQUIRED'),
        min: v => v.length >= 8 || this.$t('common.REQUIRED_MIN', { min: this.$const('PASSWORD_MIN') }),
        emailRules: v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || this.$t('common.INVALID_EMAIL'),
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
        method: this.$api('ACCOUNTS_SIGNUP').method,
        url: this.$api('ACCOUNTS_SIGNUP').url,
        data: {
          username: this.username,
          password: this.password1,
          first_name: this.firstname,
          last_name: this.lastname
        },
      })
      .then(function () {
        vm.$router.push({ name: 'accounts.login' })
        vm.$dialog.notify.success(
          vm.$t('accounts.SIGNUP_COMPLETED'), {
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
