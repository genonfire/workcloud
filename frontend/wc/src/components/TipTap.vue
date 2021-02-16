<template>
  <div class="editor">

    <editor-menu-bar :editor="editor" v-slot="{ commands, isActive, getMarkAttrs }">
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
          title="test"
        >
          <img class="icon" src="@/assets/images/icons/link.svg" />
        </button>

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
  Strike,
  Underline,
  Code,
  Table,
  TableHeader,
  TableCell,
  TableRow,
  History
} from "tiptap-extensions";

export default {
  components: {
    EditorContent,
    EditorMenuBar,
  },
  props: {
    options: Object
    // content: initial text
    // editable: read only if false
  },
  data () {
    return {
      editor: null
    }
  },
  mounted () {
    this.editor = new Editor ({
      editable: this.options.editable,
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
        new Strike(),
        new Underline(),
        new Code(),
        new Table({
          resizable: true,
        }),
        new TableHeader(),
        new TableCell(),
        new TableRow(),
        new History()
      ],
      onUpdate: ({ getHTML }) => {
        this.options.content = getHTML()
      },
      content: this.options.content,
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
    }
  }
};
</script>

<style lang="scss">
  @import '@/assets/sass/main.scss'
</style>
