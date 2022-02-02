import axios from 'axios';

export const API_BASE = 'http://localhost/api/v1';

export default axios.create({
    baseURL: API_BASE,
    responseType: "json"
});