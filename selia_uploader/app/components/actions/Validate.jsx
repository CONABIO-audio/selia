import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import api from '../../services/api';
import { argsAtom } from '../../services/state';
import { useAtom } from 'jotai';

export default function Validate(props) {
    const dispatch = useDispatch();
    const [args, setArgs] = useAtom(argsAtom)

    const changeStatus = () => {
        let unvalidated = props.items.filter(item => item.status.name == "Por Validar");
        for(let i=0;i<unvalidated.length;i++) {
            dispatch({type: 'CHANGE_STATUS',
                payload:{item: unvalidated[i],
                        newStatus: {value: 'preview', name: 'Validando...'}}
            });
        }
    }

    const validateFiles = () => {
        changeStatus();
        let unvalidated = props.items.filter(item => item.status.name == "Por Validar");
        for(let i=0;i<unvalidated.length;i++) {
            let date = new Date(unvalidated[i].date)
            if(Object.keys(unvalidated[i].metadata).length) {
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
                    "captured_on_timezone": unvalidated[i].timezoneValue,
                    "media_info": unvalidated[i].metadata,
                    "collection": args.collection,
                    "sampling_event": args.sampling_event,
                    "collection_device": args.collection_device,
                    "collection_site": args.collection_site,
                    "deployment": args.deployment,
                    "collection_metadata": args.collection_metadata,
                    "mime_type": args.mime_type[0]
                }
                api.validate(data).then((resp) => {
                    dispatch({type: 'CHANGE_STATUS',
                        payload:{item: unvalidated[i],
                                newStatus: {value: 'preview', name: 'Validado'}}
                    });
                })
                .catch(err => {
                    console.log(err)
                    dispatch({type: 'CHANGE_STATUS',
                        payload:{item: unvalidated[i],
                                newStatus: {value: 'error', name: 'Error en validacion'}}
                    });
                })
            } else {
                dispatch({type: 'CHANGE_STATUS',
                    payload:{item: unvalidated[i],
                            newStatus: {value: 'error', name: 'Error en metadata de archivo'}}
                });
            }
        }
    }

    useEffect(() => {
        if(props.items.filter(item => item.status.name == "Por Validar").length) {
            validateFiles()
        }
    });

    return null;
}