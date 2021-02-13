import { mapState } from 'vuex'

var FormatDate = {
  computed: {
    ...mapState([
      'date_format'
    ])
  },
  methods: {
    formatDate: function (dateIn) {
      var date = dateIn.split('-')

      if (this.date_format == 'YYYY/MM/DD') {
        return [date[0], date[1], date[2]].join('/')
      }
      else if (this.date_format == 'MM/DD/YYYY') {
        return [date[1], date[2], date[0]].join('/')
      }
      else if (this.date_format == 'DD/MM/YYYY') {
        return [date[2], date[1], date[0]].join('/')
      }
      else {
        return [date[0], date[1], date[2]].join('-')
      }
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
