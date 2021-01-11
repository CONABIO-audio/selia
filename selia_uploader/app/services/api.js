import axios from 'axios';

export default {
    validate(data) {
        return axios({
            method: 'post',
            url: 'http://irekuaapi-env.eba-gj4jy7ue.us-west-2.elasticbeanstalk.com/api/collections/v1/collection_items/validate/',
            data: data,
            auth: {
                username: 'jdonlucas',
                password: 'jdonlucas'
            }
        })
    }
}