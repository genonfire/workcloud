<template>
<v-container>
  <SettingMenu/>

  <div
    class="content text-center"
    v-if="initialized"
  >
    <v-simple-table>
      <thead class="device_management">
        <tr>
          <th>{{ $t('accounts.DEVICE') }}</th>
          <th>{{ $t('accounts.BROWSER') }}</th>
          <th>{{ $t('accounts.IP') }}</th>
          <th>{{ $t('accounts.LAST_LOGIN') }}</th>
          <th>{{ $t('accounts.MANAGE') }}</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="device in devices"
          :key="device.id"
        >
          <td>{{ device.device }} ({{ device.os }})</td>
          <td>{{ device.browser }}</td>
          <td>{{ device.ip_address }}</td>
          <td>{{ device.last_login }}</td>
          <td>
            <v-btn
              text
              disabled
              v-if="login_device.id === device.id"
            >
              {{ $t('accounts.THIS_DEVICE') }}
            </v-btn>
            <v-btn
              :model="device.id"
              small
              @click="deleteDevice(device)"
              v-else
            >
              {{ $t('accounts.LOGOUT') }}
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-simple-table>
  </div>

</v-container>
</template>

<style lang="scss">
thead.device_management th {
  text-align: center !important;
  background-color: #eee;
}
</style>

<script>
import SettingMenu from '../../components/SettingMenu'
import axios from 'axios'
import { mapState } from 'vuex';

export default {
  components: {
    SettingMenu,
  },

  data () {
    return {
      firstInit: false,
      devices: [],
    }
  },
  computed: {
    ...mapState([
      'login_device'
    ]),
    initialized () {
      return this.firstInit
    }
  },
  mounted () {
    var vm = this

    axios({
      method: this.$api('ACCOUNTS_DEVICES').method,
      url: this.$api('ACCOUNTS_DEVICES').url
    })
    .then(function (response) {
      var data = response.data['data']
      vm.devices = data

      vm.firstInit = true
    })
    .catch(function () {
    })
  },
  methods: {
    deleteDevice(device) {
      if (!confirm(this.$t("accounts.LOGOUT_DEVICE"))) {
        return
      }

      var vm = this

      axios({
        method: this.$api('ACCOUNTS_DEVICE_DELETE').method,
        url: this.$api('ACCOUNTS_DEVICE_DELETE').url.replace(
          '{pk}', device.id
        )
      })
      .then(function () {
        var index = vm.devices.indexOf(device)
        vm.devices.splice(index, 1)
      })
      .catch(function () {
      })
    }
  }
}
</script>
