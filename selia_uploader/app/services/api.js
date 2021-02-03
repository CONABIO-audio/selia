import axios from 'axios';
import Cookies from 'js-cookie';

export const models = {
    collection: "/api/collections/v1/collections/",
    sampling_event: "/api/collections/v1/sampling_events/",
    deployment: "/api/collections/v1/deployments/",
    collection_device: "/api/collections/v1/collection_devices/",
    collection_site: "/api/collections/v1/collection_sites/",
    licence: "/api/items/v1/licences/",
    item_type: "/api/items/v1/item_types/"
}

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
    },
    getItems() {
        return new Promise((resolve)=>{
                let elements = {}; 
                Object.entries(args).forEach(async ([key, value],index,array) => {
                        const [result] = await Promise.all([this.getObjects(key,value)])
                
                        if(key == 'deployment') {
                            elements['collection_metadata'] = result.data.collection_metadata
                            const [deployment, sampling, device] = await Promise.all([
                                this.getObjects(result.data.deployment_type.url),
                                this.getObjects(result.data.sampling_event.url),
                                this.getObjects(result.data.collection_device.url)
                            ])
                            elements['deployment'] = [deployment.data.id,deployment.data.name];

                            const [sampling_event_type,collection_site] = await Promise.all([
                                this.getObjects(sampling.data.sampling_event_type.url),
                                this.getObjects(sampling.data.collection_site.url)
                            ]) 
                            elements['sampling_event'] = [sampling_event_type.data.id,sampling_event_type.data.name];
                            elements['collection_site'] = [collection_site.data.id,collection_site.data.collection_name];
                            elements['collection_device'] = [device.data.id,device.data.collection_metadata["Nombres originales"]];
                        } else if (key == 'collection') {
                            elements['collection'] = [result.data.id,result.data.name];
                        } else if (key == 'item_type') {
                            elements['item_type'] = [result.data.id,result.data.name];
                            elements['mime_type'] = [result.data.mime_types[0].id,result.data.mime_types[0].mime_type]
                        } else if (key == 'licence') {
                            elements['licence'] = [result.data.id,result.data.licence_type.name];
                        }
                        if(Object.entries(elements).length == 9) resolve(elements)
                })
            });
    },
    getObjects(model,id) {
        let url = id ? 
                //'http://irekuaapi-env.eba-gj4jy7ue.us-west-2.elasticbeanstalk.com' + models[model] + id + '/':
                'http://localhost:8000' + models[model] + id + '/':
                model;
        const csrftoken = Cookies.get('csrftoken');
        return axios({
            method: 'get',
            url: url, 
            withCredentials: true,   
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
    }
}