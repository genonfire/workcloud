<template>
  <v-app>
    <v-main>
      <default-bar />
      <router-view />
      <default-footer />
    </v-main>
  </v-app>
</template>

<script setup>
import DefaultBar from './AppBar.vue'
import DefaultFooter from './Footer.vue'
</script>
