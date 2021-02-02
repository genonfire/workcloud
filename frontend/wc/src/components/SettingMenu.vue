<template>
  <v-tabs
    grow
    icons-and-text
    class="elevation-2"
  >
    <v-tab
      :to="{ name: 'accounts.profile' }"
    >
      {{ $t('accounts.PROFILE' )}}
      <v-icon>mdi-account</v-icon>
    </v-tab>

    <v-tab
      :to="{ name: 'accounts.devices' }"
    >
      {{ $t('accounts.MANAGE_DEVICES' )}}
      <v-icon>mdi-cellphone-link</v-icon>
    </v-tab>

    <v-tab
      :to="{ name: 'accounts.change_password' }"
    >
      {{ $t('accounts.CHANGE_PASSWORD' )}}
      <v-icon>mdi-lock-question</v-icon>
    </v-tab>

  </v-tabs>
</template>

<style lang="scss">
.v-slide-group__prev {
  display: none !important;
}
</style>
