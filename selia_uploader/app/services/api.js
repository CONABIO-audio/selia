import axios from 'axios';

export default {
    validate(data) {
        return axios.post('http://irekuaapi-env.eba-gj4jy7ue.us-west-2.elasticbeanstalk.com/api/collections/v1/collection_items/validate/',
        data)
    }
}