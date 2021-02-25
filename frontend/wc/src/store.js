import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    key: '',
    user: '',
    login_device: ''
  },
  getters: {
    isApproved: state => {
      return state.user && state.user.is_approved
    },
    isStaff: state => {
      return state.user && state.user.is_staff
    }
  },
  mutations: {
    updateUser(state, payload) {
      if (payload.key) {
        state.key = payload.key
      }
      if (payload.user) {
        state.user = payload.user
      }
      if (payload.login_device) {
        state.login_device = payload.login_device
      }
    },
    removeUser(state) {
      state.key = ''
      state.user = ''
      state.login_device = ''
    },
    updateProfile(state, payload) {
      state.user.first_name = payload.profile.first_name
      state.user.last_name = payload.profile.last_name
      state.user.call_name = payload.profile.call_name
      state.user.email = payload.profile.email
      state.user.tel = payload.profile.tel
      state.user.address = payload.profile.address
    },
    updatePhoto(state, payload) {
      state.user.photo = payload.profile.photo
    }
  }
})
