import { createI18n } from 'vue-i18n'
import en from '@/locales/en.json'
import ko from '@/locales/ko.json'

export default createI18n({
  legacy: false,
  locale: import.meta.env.VITE_I18N_LOCALE,
  fallbackLocale: import.meta.env.VITE_I18N_FALLBACK_LOCALE,
  messages: {
    ko,
    en
  }
})
