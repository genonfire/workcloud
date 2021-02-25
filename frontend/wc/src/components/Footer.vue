<template>
  <v-footer
    absolute
    dark
    padless
    app
    class="font-weight-medium"
  >
    <v-col class="text-center">
      &copy; {{ new Date().getFullYear() }} {{ $t('info.SITENAME') }}

      <v-dialog v-model="dialog" scrollable max-width="300px">
        <template v-slot:activator="{ on }">
          <v-btn
            text
            v-on="on"
          >
            <v-icon>mdi-earth</v-icon>
            {{ locale }}
          </v-btn>
        </template>
        <v-card>

          <v-card-title>
            {{ $t('common.CHANGE_LANGUAGE') }}
          </v-card-title>
          <v-divider></v-divider>

          <v-card-text>
            <v-radio-group v-model="locale" column>
              <v-row
                v-for="(lang, i) in languages"
                :key="i"
                class="ma-1"
              >
                <v-radio
                  :label="lang.name"
                  :value="lang.code"
                >
                </v-radio>
              </v-row>
            </v-radio-group>
            {{ $t('common.CHANGE_LANGUAGE_HELP') }}
          </v-card-text>

          <v-row
            justify="center"
          >
            <v-card-actions
              class="mb-5"
            >
              <v-btn
                color="primary"
                text
                @click="changeLocale"
              >
                {{ $t('common.OK') }}
              </v-btn>
            </v-card-actions>
          </v-row>

        </v-card>
      </v-dialog>

    </v-col>
  </v-footer>
</template>

<script>
export default {
  data () {
    return {
      dialog: false,
      locale: this.$root.$i18n.locale,
      languages: this.$const('LANGUAGES')
    }
  },
  methods: {
    changeLocale: function () {
      if (this.$root.$i18n.locale != this.locale) {
        this.$root.$i18n.locale = this.locale
        localStorage.setItem('locale', this.locale)
      }
      this.dialog = false
    }
  }
}
</script>

<style lang="scss">
.v-card__text {
  padding: 0 24px 0;
}
</style>
