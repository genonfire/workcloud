<template>
  <div class="editor">

    <editor-menu-bar
      :editor="editor"
      v-slot="{ commands, isActive, getMarkAttrs }"
      v-if="!options.readonly"
    >
      <div class="menubar">

        <button
          class="menubar__button"
          @click="commands.undo"
        >
          <img class="icon" src="@/assets/images/icons/undo.svg" />
        </button>

        <button
          class="menubar__button"
          @click="commands.redo"
        >
          <img class="icon" src="@/assets/images/icons/redo.svg" />
        </button>

        <button
          class="menubar__button"
          :class="{ 'is-active': isActive.heading({ level: 1 }) }"
          @click="commands.heading({ level: 1 })"
        >
          H1
        </button>

        <button
          class="menubar__button"
          :class="{ 'is-active': isActive.heading({ level: 2 }) }"
          @click="commands.heading({ level: 2 })"
        >
          H2
        </button>

        <button
          class="menubar__button"
          :class="{ 'is-active': isActive.heading({ level: 3 }) }"
          @click="commands.heading({ level: 3 })"
        >
          H3
        </button>

        <button
          class="menubar__button"
          @click="commands.horizontal_rule"
        >
          <img class="icon" src="@/assets/images/icons/hr.svg" />
        </button>


        <button
          class="menubar__button"
          :class="{ 'is-active': isActive.bold() }"
          @click="commands.bold"
        >
          <img class="icon" src="@/assets/images/icons/bold.svg" />
        </button>

        <button
          class="menubar__button"
          :class="{ 'is-active': isActive.italic() }"
          @click="commands.italic"
        >
          <img class="icon" src="@/assets/images/icons/italic.svg" />
        </button>

        <button
          class="menubar__button"
          :class="{ 'is-active': isActive.strike() }"
          @click="commands.strike"
        >
          <img class="icon" src="@/assets/images/icons/strike.svg" />
        </button>

        <button
          class="menubar__button"
          :class="{ 'is-active': isActive.underline() }"
          @click="commands.underline"
        >
          <img class="icon" src="@/assets/images/icons/underline.svg" />
        </button>

        <button
          class="menubar__button"
          :class="{ 'is-active': isActive.code() }"
          @click="commands.code"
        >
          <img class="icon" src="@/assets/images/icons/code.svg" />
        </button>

        <button
          class="menubar__button"
          :class="{ 'is-disabled': shouldDisableButton(isActive.link()), 'is-active': isActive.link() }"
          @click.prevent="isActive.link() ? changeLinkDialog(commands.link, getMarkAttrs('link')) : addLinkDialog(commands.link, getMarkAttrs('link'))"
        >
          <img class="icon" src="@/assets/images/icons/link.svg" />
        </button>

        <v-dialog
          v-model="imageDialog"
          max-width="540"
        >
          <template v-slot:activator="{ on, attrs }">
            <button
              class="menubar__button"
              :class="options.supportImage ? '' : 'is-disabled'"
              v-bind="attrs"
              v-on="options.supportImage ? on : null"
            >
              <img class="icon" src="@/assets/images/icons/image.svg" />
            </button>
          </template>
          <v-card
            class="pa-1"
          >

            <v-tabs
              v-model="imageTab"
              grow
              text
            >
              <v-tab href="#imageTab-upload">
                {{ $t('editor.IMAGE_UPLOAD') }}
              </v-tab>
              <v-tab href="#imageTab-link">
                {{ $t('editor.IMAGE_LINK') }}
              </v-tab>
            </v-tabs>

            <v-tabs-items
              v-model="imageTab"
            >
              <v-tab-item
                key="1"
                value="imageTab-upload"
              >
                <v-card-text
                  class="mt-5"
                >
                  <v-file-input
                    v-model="selectedFile"
                    accept="image/*"
                    prepend-icon="mdi-folder-open-outline"
                    show-size
                    :placeholder="$t('editor.SELECT_FILE')"
                    @change="onFileChange"
                  >
                  </v-file-input>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="primary"
                    @click="insertImage(commands.image)"
                  >
                    {{ $t('editor.INSERT_IMAGE') }}
                  </v-btn>
                </v-card-actions>
              </v-tab-item>

              <v-tab-item
                key="2"
                value="imageTab-link"
              >
                <v-card-text
                  class="mt-5"
                >
                  <v-text-field
                    v-model="fileURL"
                    single-line
                    :label="$t('editor.PASTE_LINK')"
                    prepend-icon="mdi-web"
                  >
                  </v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="primary"
                    @click="insertImage(commands.image)"
                  >
                    {{ $t('editor.INSERT_IMAGE') }}
                  </v-btn>
                </v-card-actions>
              </v-tab-item>
            </v-tabs-items>

          </v-card>
        </v-dialog>

        <v-dialog
          v-model="videoDialog"
          max-width="540"
        >
          <template v-slot:activator="{ on, attrs }">
            <button
              class="menubar__button"
              :class="options.supportVideo ? '' : 'is-disabled'"
              v-bind="attrs"
              v-on="options.supportVideo ? on : null"
            >
              <img class="icon" src="@/assets/images/icons/youtube.svg" />
            </button>
          </template>
          <v-card
            class="pa-1"
          >
            <v-card-title
            >
              {{ $t('editor.INSERT_VIDEO') }}
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text
              class="mt-2"
            >
              <v-text-field
                v-model="videoURL"
                single-line
                :label="$t('editor.PASTE_LINK')"
                prepend-icon="mdi-youtube"
              >
              </v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                @click="insertVideo()"
              >
                {{ $t('editor.INSERT_VIDEO') }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <button
          class="menubar__button"
          :class="{ 'is-active': isActive.bullet_list() }"
          @click="commands.bullet_list"
        >
          <img class="icon" src="@/assets/images/icons/ul.svg" />
        </button>

        <button
          class="menubar__button"
          :class="{ 'is-active': isActive.ordered_list() }"
          @click="commands.ordered_list"
        >
          <img class="icon" src="@/assets/images/icons/ol.svg" />
        </button>

        <button
          class="menubar__button"
          :class="{ 'is-active': isActive.blockquote() }"
          @click="commands.blockquote"
        >
          <img class="icon" src="@/assets/images/icons/quote.svg" />
        </button>

        <button
          class="menubar__button"
          :class="{ 'is-active': isActive.code_block() }"
          @click="commands.code_block"
        >
          <img class="icon" src="@/assets/images/icons/code.svg" />
        </button>

        <button
          class="menubar__button"
          @click="commands.createTable({
            rowsCount: 3,
            colsCount: 3,
            withHeaderRow: true
          })"
        >
          <img class="icon" src="@/assets/images/icons/table.svg" />
        </button>

        <span v-if="isActive.table()">
          <button
            class="menubar__button"
            @click="commands.deleteTable"
          >
            <img class="icon" src="@/assets/images/icons/delete_table.svg" />
          </button>
          <button
            class="menubar__button"
            @click="commands.addColumnBefore"
          >
            <img class="icon" src="@/assets/images/icons/add_col_before.svg" />
          </button>
          <button
            class="menubar__button"
            @click="commands.addColumnAfter"
          >
            <img class="icon" src="@/assets/images/icons/add_col_after.svg" />
          </button>
          <button
            class="menubar__button"
            @click="commands.addRowBefore"
          >
            <img class="icon" src="@/assets/images/icons/add_row_before.svg" />
          </button>
          <button
            class="menubar__button"
            @click="commands.addRowAfter"
          >
            <img class="icon" src="@/assets/images/icons/add_row_after.svg" />
          </button>
          <button
            class="menubar__button"
            @click="commands.deleteColumn"
          >
            <img class="icon" src="@/assets/images/icons/delete_col.svg" />
          </button>
          <button
            class="menubar__button"
            @click="commands.deleteRow"
          >
            <img class="icon" src="@/assets/images/icons/delete_row.svg" />
          </button>
          <button
            class="menubar__button"
            @click="commands.toggleCellMerge"
          >
            <img class="icon" src="@/assets/images/icons/combine_cells.svg" />
          </button>
        </span>

      </div>
    </editor-menu-bar>
    <editor-content class="editor__content" :editor="editor" />
  </div>
</template>

<script>
import { DOMParser } from 'prosemirror-model'
import {
  Editor,
  EditorContent,
  EditorMenuBar,
} from "tiptap"
import {
  Blockquote,
  CodeBlock,
  HardBreak,
  Heading,
  HorizontalRule,
  OrderedList,
  BulletList,
  ListItem,
  TodoItem,
  TodoList,
  Bold,
  Italic,
  Link,
  Image,
  Strike,
  Underline,
  Code,
  Table,
  TableHeader,
  TableCell,
  TableRow,
  History,
  TrailingNode,
} from "tiptap-extensions";
import Iframe from '@/components/Iframe.js'
import axios from 'axios'

export default {
  components: {
    EditorContent,
    EditorMenuBar,
  },
  props: {
    options: Object
    // content: initial and updated text
    // readonly: read only if true
    // autoFocus: Focus the editor on init
    // supportImage: upload and link images
    // supportVideo: embed video
  },
  data () {
    return {
      editor: null,
      imageDialog: false,
      videoDialog: false,
      imageTab: null,
      fileURL: null,
      videoURL: null,
      selectedFile: null,
    }
  },
  mounted () {
    this.editor = new Editor ({
      editable: !this.options.readonly,
      extensions: [
        new Blockquote(),
        new CodeBlock(),
        new HardBreak(),
        new Heading({ levels: [1, 2, 3] }),
        new HorizontalRule(),
        new BulletList(),
        new OrderedList(),
        new ListItem(),
        new TodoItem(),
        new TodoList(),
        new Bold(),
        new Italic(),
        new Link({
          openOnClick: true,
          target: '_blank',
        }),
        new Image(),
        new Strike(),
        new Underline(),
        new Code(),
        new Table({
          resizable: true,
        }),
        new TableHeader(),
        new TableCell(),
        new TableRow(),
        new History(),
        new TrailingNode(),
        new Iframe()
      ],
      onUpdate: ({ getHTML }) => {
        this.options.content = getHTML()
      },
      content: this.options.content,
      autoFocus: this.options.autoFocus,
    })
  },
  beforeDestroy () {
    this.editor.destroy()
  },
  methods: {
    shouldDisableButton: function (isActive) {
      return !isActive & window.getSelection().isCollapsed
    },
    addLinkDialog: async function (command) {
      if (window.getSelection().isCollapsed) {
        return
      }

      let res = await this.$dialog.prompt({
        title: this.$t('editor.ADD_LINK'),
        value: 'https://',
        text: 'URL',
        actions: {
          false: {
            text: this.$t('common.CLOSE')
          },
          true: {
            color: 'primary',
            text: this.$t('common.APPLY'),
          }
        }
      })
      if (res && res != 'https://' && res != 'http://') {
        command({ href: res })
      }
    },
    changeLinkDialog: async function (command, attr) {
      let res = await this.$dialog.prompt({
        title: this.$t('editor.CHANGE_LINK'),
        value: attr.href,
        text: 'URL',
        actions: {
          false: {
            color: 'error',
            text: this.$t('editor.REMOVE_LINK')
          },
          true: {
            color: 'primary',
            text: this.$t('common.APPLY'),
          }
        }
      })
      if (res != undefined) {
        if (res == 'http://' || res == 'https://') {
          res = ''
        }
        command({ href: res })
      }
    },
    insertHTML: function ({ state, view }, value) {
      const { selection } = state
      const element = document.createElement('div')
      element.innerHTML = value.trim()
      const slice = DOMParser.fromSchema(state.schema).parseSlice(element)
      const transaction = state.tr.insert(selection.anchor, slice.content)
      view.dispatch(transaction)
    },
    insertVideo: function () {
      let vm = this
      let src = this.videoURL

      if (src.includes('youtube.com/') || src.includes('youtu.be/')) {
        axios({
          method: this.$api('YOUTUBE_OEMBED').method,
          url: this.$api('YOUTUBE_OEMBED').url.replace('{url}', src),
        })
        .then(function (response) {
          const src = response.data['html']
          vm.insertHTML(vm.editor, src)

          vm.videoURL = null
          vm.videoDialog = false
        })
      }
      else {
        let embed = '<iframe src={src}></iframe>'.replace('{src}', src)
        this.insertHTML(vm.editor, embed)
        this.videoURL = null
        this.videoDialog = false
      }
    },
    insertImage: function (command) {
      const src = this.fileURL
      command({ src })

      this.selectedFile = null
      this.fileURL = null
      this.imageDialog = false
    },
    onFileChange: function () {
      if (this.selectedFile) {
        this.uploadFile(this.selectedFile)
      }
    },
    uploadFile: function (file) {
      let vm = this
      let formData = new FormData();
      formData.append('file', file)

      axios({
        method: this.$api('FILE_UPLOAD').method,
        url: this.$api('FILE_UPLOAD').url,
        data: formData,
      })
      .then(function (response) {
        vm.fileURL = response.data['data']['file']
      })
    }
  }
}
</script>

<style lang="scss">
@import '@/assets/sass/main.scss'
</style>
