<template>
  <div>
    <v-container
      class="pa-0"
    >
      <v-text-field
        v-model="title"
        outlined
        dense
      >
      </v-text-field>
    </v-container>
    <v-container
      class="content pa-0"
    >
      <TipTap
        class="mb-5"
        :options="options"
        @keydown.enter="onTab"
      />
    </v-container>

    <v-container
      class="text-center pb-0"
    >
      <v-btn
        @click="back()"
      >
        {{ $t('common.BACK') }}
      </v-btn>

      <v-btn
        color="primary"
        class="ml-5"
        @click="save()"
      >
        {{ $t('common.SAVE') }}
      </v-btn>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'
import TipTap from '@/components/TipTap'

export default {
  components: {
    TipTap
  },
  data () {
    return {
      options: {
        content: '',
        supportImage: true,
        supportVideo: true
      },
      title: null,
      saved: false
    }
  },
  async beforeRouteLeave (to, from, next) {
    if (this.saved || (!this.title && !this.options.content)) {
      next()
    }
    else {
      const res = await this.$dialog.confirm({
        text: this.$t('editor.QUIT_EDITING'),
        actions: {
          false: {
            text: this.$t('common.CANCEL')
          },
          true: {
            color: 'primary',
            text: this.$t('common.OK'),
          }
        }
      })
      if (res) {
        next()
      }
      else {
        next(false)
      }
    }
  },
  methods: {
    onTab: function () {
      console.log('tab')
    },
    save: function () {
      var vm = this
      var forumName = this.$route.params.forum

      axios({
        method: this.$api('THREAD_WRITE').method,
        url: this.$api('THREAD_WRITE').url.replace('{forum}', forumName),
        data: {
          title: this.title,
          content: this.options.content
        }
      })
      .then(function () {
        vm.saved = true
        vm.back()

        vm.$dialog.notify.success(
          vm.$t('forum.THREAD_SAVED'), {
            position: 'bottom-right',
            timeout: 2000
          }
        )
      })
      .catch(function (error) {
        if (error.response && error.response.data) {
          for (var field in error.response.data) {
            vm.$dialog.notify.info(
              field + ': ' + error.response.data[field], {
                position: 'top-right'
              }
            )
          }
        }
      })
    },
    back: function (reset=false) {
      if (!reset) {
        var page = 1
        var q = ''
      }

      this.$router.replace({
        name: 'communities.threadPage',
        params: {
          forum: this.$route.params.forum,
          page: page
        },
        query: {
          q: q
        }
      })
    }
  }
}
</script>
