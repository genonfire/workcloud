<template>
  <div class="iframe">
    <iframe
      class="iframe__embed"
      :src="src"
    >
    </iframe>
  </div>
</template>

<script>
export default {
  props: ['node', 'updateAttrs', 'view'],
  computed: {
    src: {
      get() {
        return this.node.attrs.src
      },
      set(src) {
        this.updateAttrs({
          src
        })
      }
    },
    width: {
      get() {
        return this.node.attrs.width
      },
      set(width) {
        this.updateAttrs({
          width: width
        })
      }
    },
    height: {
      get() {
        return this.node.attrs.height
      },
      set(height) {
        this.updateAttrs({
          height: height
        })
      }
    }
  }
}
</script>

<style lang="scss">
  .iframe {
    &__embed {
      width: 640px;
      height: 360px;
      border: 0;
    }
  }
</style>
