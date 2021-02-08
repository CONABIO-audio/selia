import React from 'react';
import ActionButton from '../elements/ActionButtons';
import { faClipboardCheck } from '@fortawesome/free-solid-svg-icons';
import { useDispatch } from 'react-redux';
import api from '../../services/api';
import mediaInfo from '../../services/mediaInfo';
import { argsAtom } from '../../services/state';
import { useAtom } from 'jotai';

export default function Validate(props) {
    const dispatch = useDispatch();
    const [args, setArgs] = useAtom(argsAtom)

    const changeStatus = () => {
        for(let i=0;i<props.items.length;i++) {
            dispatch({type: 'CHANGE_STATUS',
                payload:{item: props.items[i],
                        newStatus: {value: 'preview', name: 'Validando...'}}
            });
        }
    }

    const validateFiles = () => {
        changeStatus();
        for(let i=0;i<props.items.length;i++) {
            let date = new Date(props.items[i].date)
            if(Object.keys(props.items[i].metadata).length) {
                let data = {
                    "item_type": args.item_type,
                    "licence": args.licence,
                    "captured_on": date.toISOString(),
                    "captured_on_year": date.getFullYear(),
                    "captured_on_month": date.getMonth(),
                    "captured_on_day": date.getDay(),
                    "captured_on_hour": date.getHours(),
                    "captured_on_minute": date.getMinutes(),
                    "captured_on_second": date.getSeconds(),
                    "captured_on_timezone": props.items[i].timezoneValue,
                    "media_info": props.items[i].metadata,
                    "collection": args.collection,
                    "sampling_event": args.sampling_event,
                    "collection_device": 29,//args.collection_device,
                    "collection_site": args.collection_site,
                    "deployment": args.deployment,
                    "collection_metadata": args.collection_metadata,
                    "mime_type": args.mime_type[0]
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
            } else {
                dispatch({type: 'CHANGE_STATUS',
                    payload:{item: props.items[i],
                            newStatus: {value: 'error', name: 'Error en metadata de archivo'}}
                });
            }
        }
    }

    return (
        <ActionButton name='Validar archivos' icon={faClipboardCheck} 
        action={() => validateFiles()} statusType='Por Validar' align='210px' />
    )
}