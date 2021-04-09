<template>
<v-container>
  <SettingMenu/>

  <div
    class="content text-center"
    v-if="initialized"
  >
    <v-form
      v-model="validation"
    >

      <v-row justify="center">
        <v-col
          cols="50"
          md="6"
        >
          <v-row justify="space-around">
            <v-col
              class="mb-7"
            >
              <v-card
                flat
                color="deep-purple lighten-3"
                width="80"
                height="80"
                v-if="photo"
              >
                <v-img
                  :src="photo"
                  max-width="80"
                  max-height="80"
                ></v-img>
                <v-card-actions
                  class="pt-1"
                >
                  <v-btn
                    text
                    color="deep-purple accent-4"
                    class="pa-0"
                    @click="removePhoto"
                    v-if="photo"
                  >
                    {{ $t('accounts.DELETE_PHOTO') }}
                </v-btn>
                </v-card-actions>
              </v-card>
              <v-card
                width="80"
                height="80"
                class="pt-4"
                v-else
              >
                <v-icon x-large>mdi-account </v-icon>
              </v-card>
            </v-col>
            <v-col>
              <v-file-input
                v-model="file_photo"
                accept="image/*"
                prepend-icon="mdi-camera"
                show-size
                :label="$t('accounts.PHOTO')"
                :placeholder="$t('accounts.UPLOAD_PHOTO')"
                @change="onFileChange"
              >
              </v-file-input>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <v-row justify="center">
        <v-col
          cols="50"
          md="6"
        >
          <v-text-field
            v-model="user.username"
            :label="$t('accounts.USERNAME')"
            disabled
          >
          </v-text-field>
        </v-col>
      </v-row>

      <v-row justify="center">
        <v-col
          cols="50"
          md="6"
        >
          <v-text-field
            v-model="user.email"
            :rules="[rules.required, rules.emailRules]"
            :label="$t('accounts.EMAIL')"
            :hint="$t('accounts.DIFFERENT_EMAIL_HINT')"
          >
          </v-text-field>
        </v-col>
      </v-row>

      <v-row justify="center">
        <v-col
          cols="12"
          sm="3"
        >
          <v-text-field
            v-model="user.first_name"
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
            v-model="user.last_name"
            :counter="20"
            :rules="[rules.required]"
            :label="$t('accounts.LASTNAME')"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row justify="center">
        <v-col
          cols="50"
          md="6"
        >
          <v-text-field
            v-model="user.call_name"
            :counter="40"
            :rules="[rules.required]"
            :label="$t('accounts.CALLNAME')"
          >
          </v-text-field>
        </v-col>
      </v-row>

      <v-row justify="center">
        <v-col
          cols="50"
          md="6"
        >
          <v-text-field
            v-model="user.tel"
            :label="$t('accounts.TEL')"
          >
          </v-text-field>
        </v-col>
      </v-row>

      <v-row justify="center">
        <v-col
          cols="50"
          md="6"
        >
          <v-text-field
            v-model="user.address"
            :label="$t('accounts.ADDRESS')"
          >
          </v-text-field>
        </v-col>
      </v-row>

      <v-btn
        color="primary"
        @click="submit"
      >
        {{ $t('common.MODIFY') }}
      </v-btn>

    </v-form>

  </div>
</v-container>
</template>

<script>
import axios from 'axios'
import SettingMenu from '@/components/SettingMenu'
import { mapState } from 'vuex'

export default {
  components: {
    SettingMenu,
  },

  data () {
    return {
      photo: '',
      file_photo: null,
      firstInit: false,
      validation: false,
      rules: {
        required: v => !!v || this.$t('common.REQUIRED'),
        emailRules: v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || this.$t('common.INVALID_EMAIL'),
      },
    }
  },
  computed: {
    ...mapState([
      'user'
    ]),
    initialized () {
      return this.firstInit
    }
  },
  mounted () {
    var vm = this

    axios({
      method: this.$api('ACCOUNTS_SETTING_GET').method,
      url: this.$api('ACCOUNTS_SETTING_GET').url
    })
    .then(function (response) {
      var data = response.data['data']

      vm.user.first_name = data.first_name
      vm.user.last_name = data.last_name
      vm.user.call_name = data.call_name
      vm.user.email = data.email
      vm.user.tel = data.tel
      vm.user.address = data.address
      vm.photo = data.photo

      vm.firstInit = true
    })
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
        method: this.$api('ACCOUNTS_SETTING_SET').method,
        url: this.$api('ACCOUNTS_SETTING_SET').url,
        data: {
          first_name: this.user.first_name,
          last_name: this.user.last_name,
          call_name: this.user.call_name,
          email: this.user.email,
          tel: this.user.tel,
          address: this.user.address
        },
      })
      .then(function (response) {
        var data = response.data['data']

        vm.$store.commit({
          type: 'updateProfile',
          profile: data,
        })
        vm.$dialog.notify.success(
          vm.$t('common.UPDATED'), {
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
    },
    updatePhoto(data) {
      var vm = this

      axios({
        method: this.$api('ACCOUNTS_SETTING_SET').method,
        url: this.$api('ACCOUNTS_SETTING_SET').url,
        data: data,
      })
      .then(function (response) {
        var data = response.data['data']

        vm.$store.commit({
          type: 'updatePhoto',
          profile: data,
        })

        vm.photo = data.photo
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
    },
    removePhoto() {
      this.updatePhoto({ photo: null })
      this.file_photo = null
    },
    onFileChange() {
      if (this.file_photo) {
        var formData = new FormData();
        formData.append('photo', this.file_photo)

        this.updatePhoto(formData)
      }
    },
  }
}
</script>
