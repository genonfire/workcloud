import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    key: null,
    user: null,
    login_device: null
  }),
  getters: {
    isApproved(state) {
      return state.user && state.user.is_approved
    },
    isStaff(state) {
      return state.user && state.user.is_staff
    }
  },
  actions: {
    updateUser(key, user, login_device) {
      if (key) {
        this.key = key
      }
      if (user) {
        this.user = user
      }
      if (login_device) {
        this.login_device = login_device
      }
    },
    removeUser() {
      this.key = null
      this.user = null
      this.login_device = null
    },
    updateProfile(user) {
      this.user.first_name = user.first_name
      this.user.last_name = user.last_name
      this.user.call_name = user.call_name
      this.user.email = user.email
      this.user.tel = user.tel
      this.user.address = user.address
    },
    updatePhoto(user) {
      this.user.photo = user.photo
    }
  }
})
