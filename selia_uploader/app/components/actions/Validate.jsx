import React from 'react';
import ActionButton from '../elements/ActionButtons';
import { faClipboardCheck } from '@fortawesome/free-solid-svg-icons';
import { useDispatch } from 'react-redux';
import api from '../../services/api';

export default function Validate(props) {
    const dispatch = useDispatch();

    const validateFiles = () => {
        for(let i=0;i<props.items.length;i++) {
            let date = new Date(props.items[i].date)
            let data = {
                "item_type": 146,
                "licence": 1,
                "captured_on": date.toISOString(),
                "captured_on_year": date.getFullYear(),
                "captured_on_month": date.getMonth(),
                "captured_on_day": date.getDay(),
                "captured_on_hour": date.getHours(),
                "captured_on_minute": date.getMinutes(),
                "captured_on_second": date.getSeconds(),
                "captured_on_timezone": "America/Mexico_City",
                "media_info": { "image_width": 200, "image_length": 200, "datetime_original": date.toISOString() },
                "collection": 2,
                "sampling_event": null,
                "collection_device": null,
                "collection_site": null,
                "deployment": null,
                "collection_metadata": '',
                "mime_type": 50
            }
            api.validate(data).then((resp) => {
                dispatch({type: 'CHANGE_STATUS',
                    payload:{item: props.items[i],
                            newStatus: {value: 'preview', name: 'Validado'}}
                });
            })
            .catch(err => {
                console.log(err)
                dispatch({type: 'CHANGE_STATUS',
                    payload:{item: props.items[i],
                            newStatus: {value: 'error', name: 'Error en validacion'}}
                });
            })
        }
    }

    return (
        <ActionButton name='Validar archivos' icon={faClipboardCheck} 
        action={() => validateFiles()} statusType='Por Validar' align='210px' />
    )
}