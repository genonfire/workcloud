<template>

  <v-app v-if="initialized">
    <Navigation/>

    <v-main>
      <v-container fluid>
        <v-fade-transition appear
          :hide-on-leave="true"
        >
          <router-view/>
        </v-fade-transition>
      </v-container>
    </v-main>

    <Footer/>
  </v-app>

  <div class="uninitialized" v-else>
    <v-progress-circular
      :size="70"
      :width="7"
      indeterminate
      color="#4CAF50"
    ></v-progress-circular>
  </div>

</template>

<script>
import Navigation from './components/Navigation'
import Footer from './components/Footer'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    Navigation,
    Footer,
  },
  metaInfo () {
    return {
      title: this.$t('info.SITENAME')
    }
  },
  data () {
    return {
      firstInit: false,
    }
  },
  computed: {
    initialized () {
      return this.firstInit
    }
  },
  mounted () {
    var vm = this

    var local_key = localStorage.getItem('token')

    var localePattern = ''
    if (this.$const('DEFAULT_LANGUAGE') != this.$root.$i18n.locale) {
      localePattern = this.$root.$i18n.locale + '/'
    }
    axios.defaults.baseURL = (
      this.$baseURL() + localePattern + this.$apiPrefix()
    )

    if (local_key) {
      axios({
        method: this.$api('ACCOUNTS_CONNECT').method,
        url: this.$api('ACCOUNTS_CONNECT').url,
        headers: {
          Authorization: 'Token ' + local_key
        }
      })
      .then(function (response) {
        axios.defaults.headers.common['Authorization'] = 'Token ' + local_key

        vm.$store.commit({
          type: 'updateUser',
          key: local_key,
          user: response.data['data']['user'],
          login_device: response.data['data']['login_device']
        })

        vm.firstInit = true
      })
      .catch(function (error) {
        if (error.response.status === 401) {
          localStorage.clear()
        }
        vm.firstInit = true
      })
    }
    else {
      this.firstInit = true
    }
  }
}
</script>

<style lang="scss">
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.content {
  padding: 20px;
}

.uninitialized {
  text-align: center;
  margin: 5em;
}

.cursor-pointer {
  cursor: pointer;
}

pre code {
  display: block;
  background: #f6f6f6;
  white-space: pre-wrap;
  overflow-x: scroll;
  margin-top: 1em;
  margin-bottom: 1em;
}

img {
  max-width: 100%;
}
</style>
