<template>
  <v-app-bar
    app
  >
    <v-app-bar-nav-icon
      @click="drawer = !drawer"
    ></v-app-bar-nav-icon>

    <router-link :to="{ name: 'home' }">
      <v-img
        src="@/assets/images/logo.png"
        width="50"
      ></v-img>
    </router-link>
  </v-app-bar>

  <v-navigation-drawer
    v-model="drawer"
  >
  </v-navigation-drawer>

</template>

<script setup>
import { ref } from 'vue'

let drawer = ref(null)
</script>
