<template>
  <v-container>
    <div
      v-if="initialized"
      class="content pa-0"
    >
      <v-dialog
        v-model="personDialog"
        max-width="800"
        transition="dialog-bottom-transition"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-simple-table>
            <tbody>
              <tr
                v-for="person in people"
                :key="person.id"
                class="pa-0 text-center"
                v-bind="attrs"
                v-on="on"
                @click="initializePerson(person)"
              >
                <td
                  width="50"
                  class="px-2"
                >
                  <img
                    width="32"
                    height="32"
                    :src="person.photo"
                    v-if="person.photo"
                  />
                </td>
                <td>
                  {{ person.call_name }}
                </td>
                <td
                  v-if="!isMobile"
                >
                  {{ person.username }}
                </td>
                <td
                  v-if="!isMobile"
                >
                  {{ person.tel }}
                </td>
              </tr>
            </tbody>
          </v-simple-table>
        </template>

        <v-container
          class="text-center pa-2"
        >
          <v-card
            class="pa-2"
            v-if="selectedPerson"
          >
            <v-row
              class="px-2"
            >
              <v-col>
                <v-img
                  :src="selectedPerson.photo"
                  max-width="120"
                  max-height="120"
                ></v-img>
              </v-col>
              <v-col>
                <v-text-field
                  v-model="selectedPerson.username"
                  :label="$t('accounts.EMAIL')"
                  :readonly="true"
                >
                </v-text-field>
                <v-text-field
                  v-model="selectedPerson.call_name"
                  :label="$t('accounts.CALLNAME')"
                  :readonly="!user.is_staff"
                >
                </v-text-field>
              </v-col>
            </v-row>

            <v-row
              class="px-2"
            >
              <v-col
              >
                <v-text-field
                  v-model="selectedPerson.first_name"
                  :label="$t('accounts.FIRSTNAME')"
                  :readonly="!user.is_staff"
                ></v-text-field>
              </v-col>
              <v-col
              >
                <v-text-field
                  v-model="selectedPerson.last_name"
                  :label="$t('accounts.LASTNAME')"
                  :readonly="!user.is_staff"
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row
              class="px-2"
            >
              <v-col
              >
                <v-text-field
                  v-model="selectedPerson.tel"
                  :label="$t('accounts.TEL')"
                  :readonly="!user.is_staff"
                >
                </v-text-field>
              </v-col>
            </v-row>

            <v-row
              class="px-2"
            >
              <v-col
              >
                <v-text-field
                  v-model="selectedPerson.address"
                  :label="$t('accounts.ADDRESS')"
                  :readonly="!user.is_staff"
                >
                </v-text-field>
              </v-col>
            </v-row>

            <v-row
              justify="center"
              class="mx-2 pt-5 pb-1 my-1"
              v-if="user.is_staff"
            >
              <v-btn
                color="primary"
                @click="editPerson(selectedPerson)"
              >
                {{ $t('common.MODIFY') }}
              </v-btn>
            </v-row>

          </v-card>
        </v-container>

      </v-dialog>

      <Pagination
        :pagination="pagination"
        :first="getPeople"
        :prev="getPeople"
        :next="getPeople"
      />

    </div>
  </v-container>
</template>

<script>
import axios from 'axios'
import Pagination from '@/components/Pagination'
import Mobile from '@/mixins/mobile'
import { mapState } from 'vuex'

export default {
  mixins: [
    Mobile
  ],
  components: {
    Pagination
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
      personDialog: false,
      selectedPerson: null,
      people: null,
      person: null,
      firstInit: false
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
    this.getPeople(null, this.$route.query.q)
  },
  methods: {
    initializePerson (person) {
      this.selectedPerson = person
    },
    editPerson: function (person) {
      var vm = this

      axios({
        method: this.$api('ACCOUNTS_USER_EDIT').method,
        url: this.$api('ACCOUNTS_USER_EDIT').url.replace(
          '{pk}', person.id
        ),
        data: {
          first_name: person.first_name,
          last_name: person.last_name,
          call_name: person.call_name,
          tel: person.tel,
          address: person.address
        },
      })
      .then(function (response) {
        vm.selectedPerson = response.data['data']

        for (var i=0; i<vm.people.length; i++) {
          if (vm.people[i].id == vm.selectedPerson.id) {
            vm.people[i] = vm.selectedPerson
          }
        }

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
    getPeople: function (url=null, q='') {
      var vm = this

      if (!url) {
        url = this.$api('ACCOUNTS_USER_SEARCH').url + q
      }

      axios({
        method: this.$api('ACCOUNTS_USER_SEARCH').method,
        url: url
      })
      .then(function (response) {
        var pagination = response.data['pagination']
        vm.pagination.pageTotal = pagination['page_total']
        vm.pagination.currentPage = pagination['current_page']
        vm.pagination.prevLink = pagination['prev_link']
        vm.pagination.nextLink = pagination['next_link']
        vm.pagination.firstLink = pagination['first_link']

        vm.people = response.data['data']
        vm.firstInit = true
      })
    }
  }
}
</script>
