import axios from 'axios'
import { useUserStore } from '@/stores/user.js'
import CONFIG_API from '@/js/config/config.js'
import { createSingleFlight } from '@/js/utils/singleFlight.js'

const BASE_URL = CONFIG_API.HTTP_URL

// One shared refresh operation for Axios, SSE and app bootstrap.
// Keeping the token mutation here fixes a subtle bug from the old SSE path where
// refresh succeeded but the new access token was never written back into Pinia.
export const refreshAccessToken = createSingleFlight(async () => {
  const user = useUserStore()

  try {
    const res = await axios.post(
      `${BASE_URL}/api/user/account/refresh_token/`,
      {},
      { withCredentials: true, timeout: 5000 },
    )

    const access = res.data?.access
    if (!access) {
      throw new Error('refresh response missing access token')
    }

    user.setAccessToken(access)
    return access
  } catch (error) {
    user.logout()
    throw error
  }
})
