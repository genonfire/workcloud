<template>
  <v-container
    class="content"
  >
    <v-row
      justify="center"
    >
      <v-col
        v-for="(m, i) in menu"
        :key="i"
        cols="auto"
        :class="isMobile ? '' : 'mx-10'"
      >
        <v-btn
          outlined
          large
          :color="m.color"
          @click="$router.push(m.to)"
        >
          <v-icon
            class="mr-3"
          >
            {{ m.icon }}
          </v-icon>
          {{ m.text }}
        </v-btn>
      </v-col>
    </v-row>
    <v-row
      justify="center"
    >
      <v-col
        v-for="(m, i) in externalMenu"
        :key="i"
        cols="auto"
        :class="isMobile ? '' : 'mx-10'"
      >
        <v-btn
          outlined
          large
          :color="m.color"
          :href="m.url" target="_blank"
        >
          <v-icon
            class="mr-3"
          >
            {{ m.icon }}
          </v-icon>
          {{ m.text }}
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Mobile from '@/mixins/mobile'

export default {
  mixins: [
    Mobile
  ],
  data () {
    return {
    }
  },
  computed: {
    menu: function () {
      return [
        {
          text: this.$t('accounts.MANAGE_USERS'),
          icon: 'mdi-account-multiple-outline',
          color: 'indigo',
          to: { name: 'accounts.userList' }
        },
        {
          text: this.$t('forum.MANAGE_FORUM'),
          icon: 'mdi-forum-outline',
          color: 'blue-grey darken-1',
          to: { name: 'communities.forum' }
        },
        {
          text: this.$t('things.MANAGE_HOLIDAY'),
          icon: 'mdi-calendar-month',
          color: 'red darken-2',
          to: { name: 'things.holiday' }
        }
      ]
    },
    externalMenu: function () {
      return [
        {
          text: this.$t('common.SITE_ADMIN'),
          icon: 'mdi-caps-lock',
          color: 'teal darken-2',
          url: process.env.VUE_APP_API_SERVER + 'admin/'
        }
      ]
    }
  }
}
</script>
