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
              text
              disabled
              v-else-if="!device.device"
            >
              {{ $t('common.DELETED') }}
            </v-btn>
            <v-btn
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

  <Pagination
    :pagination="pagination"
    :first="getDevices"
    :prev="getDevices"
    :next="getDevices"
  />

</v-container>
</template>

<script>
import axios from 'axios'
import Pagination from '@/components/Pagination'
import SettingMenu from '@/components/SettingMenu'
import { mapState } from 'vuex'

export default {
  components: {
    Pagination,
    SettingMenu,
  },
  data () {
    return {
      pagination: {
        pageTotal: 1,
        currentPage: 1,
        firstLink: null,
        prevLink: null,
        nextLink: null
      },
      devices: [],
      firstInit: false
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
    this.getDevices()
  },
  methods: {
    getDevices: function (url=null) {
      var vm = this
      var method = 'get'

      if (!url) {
        method = this.$api('ACCOUNTS_DEVICES').method
        url = this.$api('ACCOUNTS_DEVICES').url
      }

      axios({
        method: method,
        url: url
      })
      .then(function (response) {
        var pagination = response.data['pagination']
        vm.pagination.pageTotal = pagination['page_total']
        vm.pagination.currentPage = pagination['current_page']
        vm.pagination.prevLink = pagination['prev_link']
        vm.pagination.nextLink = pagination['next_link']
        vm.pagination.firstLink = pagination['first_link']

        vm.devices = response.data['data']
        vm.firstInit = true
      })
    },
    deleteDevice: async function (device) {
      let res = await this.$dialog.warning({
        text: this.$t("accounts.LOGOUT_DEVICE"),
        actions: {
          false: this.$t('common.CANCEL'),
          true: {
            color: 'error',
            text: this.$t('accounts.LOGOUT')
          }
        }
      })
      if (!res) {
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
        vm.devices[index].device = null
      })
    }
  }
}
</script>

<style lang="scss">
thead.device_management th {
  text-align: center !important;
  background-color: #eee;
}
</style>
