<template>

  <v-container
    class="text-center mb-10"
  >
    <v-row
      justify="center"
    >
      <v-col
        class="pagination__item"
        v-if="pagination.firstLink"
      >
        <v-btn
          @click="first(pagination.firstLink)"
        >
          <v-icon>mdi-page-first</v-icon>
        </v-btn>
      </v-col>

      <v-col
        class="pagination__item"
        v-if="pagination.prevLink"
      >
        <v-btn
          color="primary"
          @click="prev(pagination.prevLink)"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-col>

      <v-col
        class="pagination__page"
      >
        <v-btn
          text
        >
          {{ pagination.currentPage }} / {{ pagination.pageTotal }}
        </v-btn>
      </v-col>

      <v-col
        class="pagination__item"
        v-if="pagination.nextLink"
      >
        <v-btn
          color="primary"
          @click="next(pagination.nextLink)"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </v-container>

</template>

<script>
export default {
  props: {
    pagination: Object,
    first: Function,
    prev: Function,
    next: Function
  }
}
</script>

<style lang="scss">
.pagination__item {
  max-width: 72px;
  width: auto;
  padding: 0;
}
.pagination__item button {
  min-width: 40px !important;
}
.pagination__page {
  max-width: 120px;
  width: auto;
  padding: 0;
}
.pagination__page button {
  font-size: 1rem !important;
}
</style>
