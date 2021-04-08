<template>
  <div
    v-if="initialized"
  >
    <v-container
      class="pa-0"
    >
      <v-text-field
        v-model="thread.title"
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
      />
    </v-container>

    <v-container
      class="text-center pb-0"
    >
      <v-btn
        @click="$router.go(-1)"
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
    <v-container
      class="text-right caption pa-0"
    >
       {{ updated_at }}
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'
import TipTap from '@/components/TipTap'
import FormatDate from '@/mixins/formatDate'

export default {
  mixins: [
    FormatDate
  ],
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
      thread: null,
      firstInit: false
    }
  },
  computed: {
    title () {
      return this.thread.title
    },
    updated_at () {
      return this.$t('editor.LAST_UPDATED_AT', {
        datetime: this.formatDateTime(this.thread.modified_at)
      })
    },
    initialized () {
      return this.firstInit
    }
  },
  mounted () {
    this.getThread(this.$route.params.pk)
  },
  async beforeRouteLeave (to, from, next) {
    if (this.thread.content == this.options.content) {
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
    save: function () {
      var vm = this
      var forumName = this.$route.params.forum

      axios({
        method: this.$api('THREAD_EDIT').method,
        url: this.$api('THREAD_EDIT').url.replace(
          '{forum}', forumName).replace('{pk}', this.thread.id),
        data: {
          title: this.title,
          content: this.options.content
        }
      })
      .then(function (response) {
        vm.thread = response.data['data']

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
    getThread: function (pk) {
      var vm = this
      this.page = this.$route.params.page
      this.forumName = this.$route.params.forum

      axios({
        method: this.$api('THREAD_RETRIEVE').method,
        url: this.$api('THREAD_RETRIEVE').url.replace(
          '{forum}', this.forumName).replace('{pk}', pk)
      })
      .then(function (response) {
        vm.thread = response.data['data']
        vm.options.content = vm.thread.content
        vm.firstInit = true
      })
    }
  }
}
</script>
