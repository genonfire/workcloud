import { createI18n } from 'vue-i18n'
import en from '@/locales/en.json'
import ko from '@/locales/ko.json'

export default createI18n({
  legacy: false,
  locale: 'ko',
  messages: {
    ko,
    en
  }
})
