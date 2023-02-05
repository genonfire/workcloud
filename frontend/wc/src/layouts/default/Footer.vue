<template>
  <v-footer
    app
    theme="dark"
  >
    <v-col class="text-center">
      &copy; {{ new Date().getFullYear() }} <strong>{{ $t('info.SITENAME') }}</strong>
    </v-col>
  </v-footer>
</template>
