<template>
  <div
    v-if="initialized"
  >
    <v-container
      class="content pt-0"
    >

      <v-row justify="space-around">
        <v-col
          md=10
        >
          <v-sheet
            color="#eee"
            elevation="2"
            class="mb-5 pa-5"
          >
            {{ $t('things.HOLIDAY_DATA_DESCRIPTION') }}
          </v-sheet>
        </v-col>
      </v-row>

      <div
        align="center"
      >
        <span
          class="text-h3"
        >
          {{ year }}
        </span>
      </div>

      <div>
        <v-row
          justify="space-between"
          class="mx-3 pb-4 my-1"
        >
          <span>
            <v-btn
              outlined
              :loading="updating"
              :disabled="updating"
              @click="updateHoliday(year)"
            >
              <v-icon>mdi-cloud-download-outline</v-icon>
            </v-btn>
          </span>
          <span
          >
            <v-btn
              small
              :disabled="year < 2021"
              @click="getHoliday(year - 1)"
            >
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
            <v-btn
              small
              @click="getHoliday()"
            >
              {{ thisYear }}
            </v-btn>
            <v-btn
              small
              @click="getHoliday(year + 1)"
            >
              <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
          </span>
        </v-row>
      </div>

      <v-dialog
        v-model="editDialog"
        transition="dialog-bottom-transition"
        width="90%"
        :max-width="600"
      >
        <template v-slot:activator="{ on, attrs }">
          <div>
            <v-simple-table>
              <thead>
              </thead>
              <tbody>
                <tr
                  v-for="holiday in holidays"
                  :key="holiday.id"
                  v-bind="attrs"
                  v-on="on"
                  @click="initializeEditHoliday(holiday)"
                >
                  <td
                  >
                    {{ holiday.date }}
                  </td>
                  <td
                  >
                    {{ holiday.name }}
                  </td>
                </tr>
              </tbody>
            </v-simple-table>
          </div>
        </template>

        <v-container
          class="text-center"
        >
          <v-card
            v-if="holidayForEdit"
          >
            <v-card-title>
              <v-icon
                class="mx-2"
              >
                mdi-clock-time-eight-outline
              </v-icon>
              {{ $t('things.EDIT_HOLIDAY') }}
            </v-card-title>
            <v-card-text>
              <v-form
                v-model="validation"
              >
                <v-text-field
                  v-model="holidayForEdit.date"
                  :label="$t('things.EDIT_DATE_DESCRIPTION')"
                  outlined
                  class="centered-input"
                >
                </v-text-field>
                <v-textarea
                  v-model="holidayForEdit.name"
                  :label="$t('things.HOLIDAY_NAME')"
                  :rules="[rules.required]"
                  background-color="grey lighten-4"
                  auto-grow
                  outlined
                >
                </v-textarea>
              </v-form>
            </v-card-text>
              <v-row
                justify="space-between"
                class="mx-6 pb-4 my-1"
              >
                <v-btn
                  color="error"
                  @click="deleteHoliday(holidayForEdit)"
                >
                  {{ $t('common.DELETE') }}
                </v-btn>

                <v-btn
                  color="primary"
                  @click="editHoliday(holidayForEdit)"
                >
                  {{ $t('common.MODIFY') }}
                </v-btn>
              </v-row>
          </v-card>
        </v-container>

      </v-dialog>

    </v-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      editDialog: false,
      dateForEdit: null,
      nameForEdit: null,
      holidayForEdit: null,
      updating: false,
      year: '',
      thisYear: new Date().getFullYear(),
      holidays: null,
      firstInit: false,
      validation: false,
      rules: {
        required: v => !!v || this.$t('common.REQUIRED')
      },
    }
  },
  computed: {
    initialized () {
      return this.firstInit
    }
  },
  mounted () {
    this.getHoliday()
  },
  methods: {
    setYearMonth: function (date) {
      this.year = date[0]
      this.month = date[1]
    },
    initializeEditShift: function (shift) {
      this.shiftForEdit = shift
      this.reasonForEdit = null

      var timestamp = shift.timestamp.split('+')
      this.timestampForEdit = timestamp[0].replace('T', ' ')
      this.timezone = '+' + timestamp[1]
    },
    initializeEditHoliday: function (holiday) {
      this.holidayForEdit = holiday
    },
    deleteHoliday: function (holiday) {
      var vm = this

      axios({
        method: this.$api('DELETE_HOLIDAY').method,
        url: this.$api('DELETE_HOLIDAY').url.replace('{pk}', holiday.id)
      })
      .then(function () {
        var index = vm.holidays.indexOf(holiday)
        vm.holidays.splice(index, 1)

        vm.$dialog.notify.success(
          vm.$t('common.DELETED'), {
            position: 'bottom-right'
          }
        )
        vm.editDialog = false
      })
    },
    editHoliday: function (holiday) {
      if (!this.validation) {
        this.$dialog.notify.info(
          this.$t('common.INPUT_ERROR'), {
            position: 'top-right'
          }
        )
        return
      }

      var vm = this

      axios({
        method: this.$api('EDIT_HOLIDAY').method,
        url: this.$api('EDIT_HOLIDAY').url.replace('{pk}', holiday.id),
        data: {
          date: holiday.date,
          name: holiday.name
        }
      })
      .then(function (response) {
        for (var i=0; i<vm.holidays.length; i++) {
          if (!vm.holidays[i].id == holiday.id) {
            vm.holidays[i] = response.data['data']
            break
          }
        }
        vm.$dialog.notify.success(
          vm.$t('common.UPDATED'), {
            position: 'bottom-right'
          }
        )
        vm.editDialog = false
      })
      .catch(function (error) {
        if (error.response && error.response.data) {
          for (var field in error.response.data) {
            var field_text = ''
            if (field != 'non_field_errors') {
              field_text = field + ': '
            }
            vm.$dialog.notify.info(
              field_text + error.response.data[field], {
                position: 'top-right'
              }
            )
          }
        }
      })
    },
    updateHoliday: function (year) {
      var vm = this

      this.updating = true

      axios({
        method: this.$api('UPDATE_HOLIDAY').method,
        url: this.$api('UPDATE_HOLIDAY').url.replace('{year}', year)
      })
      .then(function (response) {
        if (response.data['data']) {
          vm.getHoliday(year)
        }
        else {
          vm.$dialog.notify.success(
            vm.$t('things.NO_UPDATE_FOUND'), {
              position: 'bottom-right'
            }
          )
        }
        vm.updating = false
      })
    },
    getHoliday: function (year=null) {
      var vm = this

      if (!year) {
        year = this.thisYear
      }
      this.year = year

      axios({
        method: this.$api('HOLIDAY_LIST').method,
        url: this.$api('HOLIDAY_LIST').url.replace('{year}', year)
      })
      .then(function (response) {
        vm.holidays = response.data['data']
        vm.firstInit = true
      })
    }
  }
}
</script>

<style scoped>
.centered-input >>> input {
  text-align: center
}
</style>