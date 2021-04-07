var FormatDate = {
  methods: {
    formatDateTime: function (datetime) {
      return new Date(datetime).toLocaleString(this.$root.$i18n.locale)
    },
    formatDate: function (dateIn) {
      return new Date(dateIn).toLocaleDateString(this.$root.$i18n.locale)
    },
    formatTime: function (dateIn) {
      return new Date(dateIn).toLocaleTimeString(this.$root.$i18n.locale)
    },
    getDateOrTime: function (dateOrTime) {
      if (dateOrTime.date) {
        return this.formatDate(dateOrTime.date)
      }
      else {
        return dateOrTime.time
      }
    }
  }
}

export default FormatDate
