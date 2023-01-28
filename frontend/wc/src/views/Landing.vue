<template>
  <v-container>
  </v-container>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router';

const router = useRouter()

onMounted(() => {
  router.push({ 'name': 'home' })
})
</script>
