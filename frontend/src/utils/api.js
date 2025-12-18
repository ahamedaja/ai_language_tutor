import axios from 'axios';

export function api(token) {
  const instance = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
      Authorization: token ? `Bearer ${token}` : ''
    }
  });

  return instance;
}
