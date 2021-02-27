<template>
<v-container>
  <SettingMenu/>

  <div class="content text-center">
    <v-container>
      <v-row justify="space-around">
        <v-col md=6>
          <v-sheet
            color="#eee"
            elevation="3"
            class="mb-5 pa-5"
          >
            {{ $t('accounts.PASSWORD_DESCRIPTION') }}
          </v-sheet>
        </v-col>
      </v-row>

      <v-form
        v-model="validation"
      >

        <v-row justify="center">
          <v-col cols="12" md="4">
            <v-text-field
              v-model="old_password"
              :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="[rules.required]"
              :type="show1 ? 'text' : 'password'"
              name="old_password"
              autocomplete="on"
              :label="$t('accounts.OLD_PASSWORD')"
              @click:append="show1 = !show1"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col cols="12" md="4">
            <v-text-field
              v-model="new_password"
              :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="[rules.required, rules.min, rules.passwordDifferent]"
              :type="show2 ? 'text' : 'password'"
              name="new_password"
              autocomplete="on"
              :label="$t('accounts.NEW_PASSWORD')"
              :hint="$t('common.REQUIRED_MIN', { min: $const('PASSWORD_MIN') })"
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
          {{ $t('common.CHANGE') }}
        </v-btn>

      </v-form>
    </v-container>
  </div>

</v-container>
</template>

<script>
import axios from 'axios'
import SettingMenu from '@/components/SettingMenu'

export default {
  components: {
    SettingMenu,
  },

  data () {
    return {
      validation: false,
      old_password: '',
      new_password: '',
      show1: false,
      show2: false,
      rules: {
        required: v => !!v || this.$t('common.REQUIRED'),
        min: v => v.length >= this.$const('PASSWORD_MIN') || this.$t('common.REQUIRED_MIN', { min: this.$const('PASSWORD_MIN') }),
        passwordDifferent: () => this.old_password !== this.new_password || this.$t('accounts.PASSWORD_SAME'),
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
        method: this.$api('ACCOUNTS_PASSWORD_CHANGE').method,
        url: this.$api('ACCOUNTS_PASSWORD_CHANGE').url,
        data: {
          old_password: this.old_password,
          new_password: this.new_password
        },
      })
      .then(function () {
        vm.$store.commit({
          type: 'removeUser'
        })

        localStorage.clear()

        axios.defaults.headers.common['Authorization'] = ''
        vm.$dialog.notify.success(
          vm.$t('accounts.CHANGE_PASSWORD_COMPLETED'), {
            position: 'bottom-right'
          }
        )
        vm.$router.push({ name: 'accounts.login' })
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
