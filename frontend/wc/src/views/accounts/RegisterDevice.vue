<template>
  <div
    class="content text-center"
    v-if="login_device"
  >
    <v-row justify="space-around">
      <v-col md=6>
        <v-sheet
          color="#eee"
          elevation="3"
          class="mb-5 pa-5"
        >
          {{ $t('accounts.REGISTER_DEVICE') }}
          <v-row
            justify="center"
            class="mt-5"
          >
            <v-chip class="ma-2" color="primary">
              {{ login_device.device }}
            </v-chip>
            <v-chip class="ma-2" color="secondary">
              {{ login_device.os }}
            </v-chip>
            <v-chip class="ma-2" color="secondary">
              {{ login_device.browser }}
            </v-chip>
            <v-chip class="ma-2" color="primary">
              {{ login_device.ip_address }}
            </v-chip>
          </v-row>
        </v-sheet>
      </v-col>
    </v-row>
    <v-btn
      color="success"
      @click="register"
    >
      {{ $t('common.REGISTER') }}
    </v-btn>
    <v-btn
      :to="{ name: 'home' }"
      color="error"
      class="ma-2"
    >
      {{ $t('common.NO') }}
    </v-btn>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState([
      'key',
      'login_device'
    ]),
    get_device: function () {
      return this.login_device.device + '(' + this.login_device.os + ') ' + this.login_device.browser + ' ' + this.login_device.ip_address
    }
  },
  methods: {
    register: function () {
      var vm = this

      axios({
        method: this.$api('ACCOUNTS_DEVICE_REGISTER').method,
        url: this.$api('ACCOUNTS_DEVICE_REGISTER').url.replace(
          '{pk}', this.login_device.id
        )
      })
      .then(function () {
        localStorage.setItem('token', vm.key)
        vm.$router.push({ name: 'home' })
      })
    }
  }
}
</script>
