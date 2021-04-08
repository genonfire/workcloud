import { Node } from 'tiptap'
import IframeView from '@/components/IframeView'

export default class Iframe extends Node {
  get name() {
    return 'iframe'
  }

  get schema() {
    return {
      attrs: {
        src: {
          default: null
        },
        width: {
          default: 640
        },
        height: {
          default: 360
        }
      },
      group: 'block',
      selectable: false,
      parseDOM: [{
        tag: 'iframe',
        getAttrs: dom => ({
          src: dom.getAttribute('src'),
          width: dom.getAttribute('width') || 640,
          height: dom.getAttribute('height') || 360
        }),
      }],
      toDOM: node => ['iframe', {
        src: node.attrs.src,
        width: node.attrs.width,
        height: node.attrs.height,
        frameborder: 0,
        allowfullscreen: 'true',
        allow: 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
      }]
    }
  }

  get view() {
    return IframeView
  }
}
