import axios from 'axios';
import config from "./config";

const refreshToken = async () => {
  try {
    const refresh_token = localStorage.getItem('_r');
    const baseURL = config.baseURL;
      let refreshEndpoint = "token/refresh/";

    if (refresh_token) {
      const response = await axios.post(`${baseURL}${refreshEndpoint}`, {
        refresh: refresh_token,
      });

      const new_access_token = response.data.access;

      // Update localStorage with the new access token
      localStorage.setItem('_a', new_access_token);

      return new_access_token;
    }
  } catch (error) {
    console.error('Error refreshing token:', error);
    throw error;
  }
};

export default refreshToken;
