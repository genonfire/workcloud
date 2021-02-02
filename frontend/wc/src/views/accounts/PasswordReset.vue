<template>
  <div
    class="content text-center"
    v-if="done"
  >
    <v-row justify="space-around">
      <v-col md=6>
        <v-sheet
          color="#eee"
          elevation="3"
          class="mb-5 pa-5"
        >
          {{ $t('accounts.PASSWORD_EMAIL_DESCRIPTION') }}
        </v-sheet>
      </v-col>
    </v-row>
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
          {{ $t('accounts.PASSWORD_RESET_DESCRIPTION') }}
        </v-sheet>
      </v-col>
    </v-row>

    <v-form
      v-model="validation"
    >

      <v-row justify="center">
        <v-col
          cols="50"
          md="6"
        >
          <v-text-field
            v-model="email"
            :rules="[rules.required, rules.emailRules]"
            :label="$t('accounts.EMAIL')"
            :hint="$t('common.EMAIL_TYPE')"
          >
          </v-text-field>
        </v-col>
      </v-row>

      <v-btn
        color="primary"
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
        email_sent: false,
        email: '',
        rules: {
          required: v => !!v || this.$t('common.REQUIRED'),
          emailRules: v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || this.$t('common.INVALID_EMAIL'),
        },
      }
    },
    computed: {
      done () {
        return this.email_sent
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
          method: 'post',
          url: '/accounts/password_reset/',
          data: {
            email: this.email
          },
        })
        .then(function () {
          vm.email_sent = true
        })
        .catch(function (error) {
          if (error.response && error.response.data) {
            for (var field in error.response.data) {
              vm.$dialog.notify.info(
                error.response.data[field], {
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
