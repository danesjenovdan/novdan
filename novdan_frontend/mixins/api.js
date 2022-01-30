function api() {
  if (typeof window === 'undefined') {
    return
  }

  const tokens = {
    clientId: this.$config.apiClientId,
    get accessToken() {
      return localStorage.getItem('dash_access_token')
    },
    get refreshToken() {
      return localStorage.getItem('dash_refresh_token')
    }
  }

  // create axios instance with api base url
  const plainApi = this.$axios.create({ baseURL: this.$config.apiBase })
  const authedApi = this.$axios.create({ baseURL: this.$config.apiBase })

  // automatically add auth header to all api requests
  authedApi.interceptors.request.use((config) => {
    config.headers.Authorization = `Bearer ${tokens.accessToken}`
    return config
  })

  const refreshAuth = async () => {
    if (!tokens.refreshToken) {
      throw new Error('Missing refresh token')
    }

    // using URLSearchParams forces content type `application/x-www-form-urlencoded`
    const params = new URLSearchParams()
    params.append('client_id', tokens.clientId)
    params.append('grant_type', 'refresh_token')
    params.append('refresh_token', tokens.refreshToken)

    const data = await plainApi.$post('/o/token/', params)
    localStorage.setItem('dash_access_token', data.access_token)
    localStorage.setItem('dash_refresh_token', data.refresh_token)
  }

  // refresh the token and retry if request fails with 401 (Unauthorized)
  authedApi.interceptors.response.use(null, async (error) => {
    if (error.config && error.response.status === 401) {
      // try refreshing the access token
      try {
        await refreshAuth()
      } catch (e) {
        // refresh failed; just reject with the original error
        return Promise.reject(error)
      }
      // retry the same request again
      return authedApi(error.config)
    }
    // rejecting with the error is the default behaviour
    return Promise.reject(error)
  })

  return {
    hasToken() {
      return tokens.accessToken && tokens.refreshToken
    },
    async login(username, password) {
      // using URLSearchParams forces content type `application/x-www-form-urlencoded`
      const params = new URLSearchParams()
      params.append('client_id', tokens.clientId)
      params.append('grant_type', 'password')
      params.append('username', username)
      params.append('password', password)

      const data = await plainApi.$post('/o/token/', params)
      localStorage.setItem('dash_access_token', data.access_token)
      localStorage.setItem('dash_refresh_token', data.refresh_token)
    },
    async register(username, email, password, confirmPassword) {
      // using URLSearchParams forces content type `application/x-www-form-urlencoded`
      const params = new URLSearchParams()
      params.append('client_id', tokens.clientId)
      params.append('grant_type', 'password')
      params.append('username', username)
      params.append('email', email)
      params.append('password', password)
      params.append('confirm_password', confirmPassword)

      /* eslint-disable no-unused-vars */
      const response = await plainApi.$post('/api/register', params)

      // login
      await this.login(username, password)
    },
    async logout() {
      const token = tokens.refreshToken || tokens.accessToken
      if (!token) {
        return
      }

      // using URLSearchParams forces content type `application/x-www-form-urlencoded`
      const params = new URLSearchParams()
      params.append('client_id', tokens.clientId)
      params.append('token', token)

      try {
        await plainApi.$post('/o/revoke_token/', params)
        localStorage.removeItem('dash_access_token')
        localStorage.removeItem('dash_refresh_token')
      } catch (e) {}
    },
    getStatus() {
      return authedApi.$get('/api/status')
    },
    activateSubscription() {
      return authedApi.$get('/api/subscription/activate')
    },
    activateSubscription2(nonce) {
      const params = new URLSearchParams()
      params.append('client_id', tokens.clientId)
      params.append('nonce', nonce)
      return authedApi.$post('/api/subscription/activate', params)
    },
    cancelSubscription() {
      return authedApi.$post('/api/subscription/cancel')
    },
    changePassword(oldPassword, newPassword) {
      return authedApi.$post('/api/change-password', {
        new_password: newPassword,
        old_password: oldPassword
      })
    },
    connectExtension() {
      return authedApi.$post('/api/connect-extension', {})
    }
  }
}

export default {
  created() {
    const $api = api.call(this)
    Object.defineProperty(this, '$api', {
      get() {
        return $api
      }
    })
  }
}
