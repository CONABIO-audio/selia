import axios from 'axios';
import Cookies from 'js-cookie';

export default {
    validate(data) {
        const csrftoken = Cookies.get('csrftoken');
        return axios({
            method: 'post',
            url: 'http://localhost:5001/api/collections/v1/collection_items/validate/',
            //url: "http://irekuaapi-env.eba-gj4jy7ue.us-west-2.elasticbeanstalk.com/api/collections/v1/collection_items/validate/", 
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
            url: 'http://localhost:5001/api/collections/v1/collection_items/',
            //url: "http://irekuaapi-env.eba-gj4jy7ue.us-west-2.elasticbeanstalk.com/api/collections/v1/collection_items/", 
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