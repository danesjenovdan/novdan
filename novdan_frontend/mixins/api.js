function api() {
  if (typeof window === "undefined") {
    return;
  }

  const tokens = {
    clientId: this.$config.apiClientId,
    get accessToken() {
      return localStorage.getItem("dash_access_token");
    },
    get refreshToken() {
      return localStorage.getItem("dash_refresh_token");
    },
  };

  const apiBase = this.$config.apiBase;

  const parseResponse = async (response) => {
    const text = await response.text();
    if (!text) {
      return null;
    }

    try {
      return JSON.parse(text);
    } catch {
      return text;
    }
  };

  const request = async (path, options = {}) => {
    const response = await fetch(`${apiBase}${path}`, options);
    const data = await parseResponse(response);

    if (!response.ok) {
      const error = new Error("Request failed");
      error.status = response.status;
      error.data = data;
      throw error;
    }

    return data;
  };

  const plainRequest = (path, { method = "GET", body, headers = {} } = {}) => {
    return request(path, {
      method,
      headers,
      body,
    });
  };

  const authedRequest = async (
    path,
    { method = "GET", body, headers = {}, retry = true } = {},
  ) => {
    const authHeaders = { ...headers };
    if (tokens.accessToken) {
      authHeaders.Authorization = `Bearer ${tokens.accessToken}`;
    }

    try {
      return await request(path, {
        method,
        headers: authHeaders,
        body,
      });
    } catch (error) {
      if (error.status === 401 && retry) {
        try {
          await refreshAuth();
        } catch {
          throw error;
        }

        return authedRequest(path, { method, body, headers, retry: false });
      }

      throw error;
    }
  };

  const refreshAuth = async () => {
    if (!tokens.refreshToken) {
      throw new Error("Missing refresh token");
    }

    // using URLSearchParams forces content type `application/x-www-form-urlencoded`
    const params = new URLSearchParams();
    params.append("client_id", tokens.clientId);
    params.append("grant_type", "refresh_token");
    params.append("refresh_token", tokens.refreshToken);

    const data = await plainRequest("/o/token/", {
      method: "POST",
      body: params,
    });
    localStorage.setItem("dash_access_token", data.access_token);
    localStorage.setItem("dash_refresh_token", data.refresh_token);
  };

  return {
    hasToken() {
      return tokens.accessToken && tokens.refreshToken;
    },
    async login(username, password) {
      // using URLSearchParams forces content type `application/x-www-form-urlencoded`
      const params = new URLSearchParams();
      params.append("client_id", tokens.clientId);
      params.append("grant_type", "password");
      params.append("username", username);
      params.append("password", password);

      const data = await plainRequest("/o/token/", {
        method: "POST",
        body: params,
      });
      localStorage.setItem("dash_access_token", data.access_token);
      localStorage.setItem("dash_refresh_token", data.refresh_token);
    },
    async register(username, email, password, confirmPassword) {
      // using URLSearchParams forces content type `application/x-www-form-urlencoded`
      const params = new URLSearchParams();
      params.append("client_id", tokens.clientId);
      params.append("grant_type", "password");
      params.append("username", username);
      params.append("email", email);
      params.append("password", password);
      params.append("confirm_password", confirmPassword);

      /* eslint-disable no-unused-vars */
      const response = await plainRequest("/api/register", {
        method: "POST",
        body: params,
      });

      // login
      await this.login(username, password);
    },
    async logout() {
      const token = tokens.refreshToken || tokens.accessToken;
      if (token) {
        // using URLSearchParams forces content type `application/x-www-form-urlencoded`
        const params = new URLSearchParams();
        params.append("client_id", tokens.clientId);
        params.append("token", token);

        try {
          await plainRequest("/o/revoke_token/", {
            method: "POST",
            body: params,
          });
          localStorage.removeItem("dash_access_token");
          localStorage.removeItem("dash_refresh_token");
        } catch {
          // ignore
        }
      }

      // logout extension
      window.postMessage({
        name: "novdan",
        event: { type: "page:logout", detail: {} },
      });
    },
    getStatus() {
      return authedRequest("/api/status");
    },
    activateSubscription(captcha) {
      const params = new URLSearchParams();
      params.append("captcha", captcha);
      return authedRequest(`/api/subscription/activate?${params}`);
    },
    activateSubscription2(nonce) {
      const params = new URLSearchParams();
      params.append("client_id", tokens.clientId);
      params.append("nonce", nonce);
      return authedRequest("/api/subscription/activate", {
        method: "POST",
        body: params,
      });
    },
    cancelSubscription() {
      return authedRequest("/api/subscription/cancel", { method: "POST" });
    },
    changePassword(oldPassword, newPassword, confirmNewPassword) {
      return authedRequest("/api/change-password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          old_password: oldPassword,
          new_password: newPassword,
          confirm_password: confirmNewPassword,
        }),
      });
    },
    connectExtension() {
      return authedRequest("/api/connect-extension", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
      });
    },
  };
}

export default {
  created() {
    const $api = api.call(this);
    Object.defineProperty(this, "$api", {
      get() {
        return $api;
      },
    });
  },
};
