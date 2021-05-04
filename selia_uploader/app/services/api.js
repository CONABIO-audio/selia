import axios from 'axios';
import Cookies from 'js-cookie';

export default {
    validate(data) {
        const csrftoken = Cookies.get('csrftoken');
        return axios({
            method: 'post',
            url: 'http://localhost:8000/api/collections/v1/collection_items/validate/',
            withCredentials: true,
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
            data: data
        })
    },
    upload(data,onUpload) {
        const csrftoken = Cookies.get('csrftoken');
        return axios({
            method: 'post',
            url: 'http://localhost:8000/api/collections/v1/collection_items/',
            withCredentials: true,
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': "multipart/form-data"
            },
            data: data,
            onUploadProgress: onUpload
        })
    }
}