import Axios from 'axios';

const post = (url, payload) => {
    return Axios.post(url, qs.stringify(payload), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' }});
};

const get = (url, payload) => {
    return Axios.get(url, qs.stringify(payload), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' }});
};

const put = (url, payload) => {
    return Axios.put(url, qs.stringify(payload), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' }});
};

const del = (url, payload) => {
    return Axios.delete(url, qs.stringify(payload), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' }});
};
