import axios from 'axios';
import Cookies from 'js-cookie';

export default {
    validate(data) {
        const csrftoken = Cookies.get('csrftoken');
        return axios({
            method: 'post',
            url: 'http://irekuaapi-env.eba-gj4jy7ue.us-west-2.elasticbeanstalk.com/api/collections/v1/collection_items/validate/',
            withCredentials: true,
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: data
        })
    }
}