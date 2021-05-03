import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import api from '../../services/api';
import ActionButton from '../elements/ActionButtons';
import { faClipboardCheck } from '@fortawesome/free-solid-svg-icons';
import { argsAtom, currentDivAtom } from '../../services/state';
import { useAtom } from 'jotai';

export const dataJson = (args,date,file) => {
    return {
        "item_type": args.item_type,
        "licence": args.licence,
        "captured_on": date.toISOString(),
        "captured_on_year": date.getFullYear(),
        "captured_on_month": date.getMonth()+1,
        "captured_on_day": date.getDate(),
        "captured_on_hour": date.getHours(),
        "captured_on_minute": date.getMinutes(),
        "captured_on_second": date.getSeconds(),
        "captured_on_timezone": file.timezoneValue,
        "media_info": file.metadata,
        "collection": args.collection,
        "sampling_event": args.sampling_event,
        "collection_device": args.collection_device,
        "collection_site": args.collection_site,
        "deployment": args.deployment,
        "collection_metadata": args.collection_metadata,
        "mime_type": args.mime_types.find(type => type[1] == file.type.replace("audio/wav","audio/x-wav"))[0]
    }
}

export default function Validate(props) {
    const dispatch = useDispatch();
    const [args, setArgs] = useAtom(argsAtom)
    const [current] = useAtom(currentDivAtom)

    const changeStatus = (status,type) => {
        let unvalidated = props.items.filter(item => item.status[type] == status);
        for(let i=0;i<unvalidated.length;i++) {
            dispatch({type: 'CHANGE_STATUS',
                payload:{item: unvalidated[i],
                        newStatus: {value: 'preview', name: 'Validando...'}}
            });
        }
    }

    const validateFiles = (status,type) => {
        changeStatus(status,type);
        let unvalidated = props.items.filter(item => item.status[type] == status);
        for(let i=0;i<unvalidated.length;i++) {
            let date = new Date(unvalidated[i].date)
            if(Object.keys(unvalidated[i].metadata).length) {
                let data = dataJson(args,date,unvalidated[i]);
                api.validate(data).then((resp) => {
                    dispatch({type: 'CHANGE_STATUS',
                        payload:{item: unvalidated[i],
                                newStatus: {value: 'preview', name: 'Validado'}}
                    });
                    dispatch({type: 'CHANGE_VALUE',
                        payload:{item: unvalidated[i],
                                field: 'error',
                                value: false
                            }
                    });
                    dispatch({type: 'CHANGE_VALUE',
                        payload:{item: unvalidated[i],
                                field: 'errorMeaning',
                                value: ''
                            }
                    });
                })
                .catch(err => {
                    let errorText = "";
                    Object.entries(err.response.data).forEach(([key,value]) => {
                        errorText = errorText + key + ": "
                        errorText = errorText + value + " "
                    })
                    dispatch({type: 'CHANGE_STATUS',
                        payload:{item: unvalidated[i],
                                newStatus: {value: 'error', name: 'Error en validacion'}}
                    });
                    dispatch({type: 'CHANGE_VALUE',
                        payload:{item: unvalidated[i],
                                field: 'error',
                                value: true
                            }
                    });
                    dispatch({type: 'CHANGE_VALUE',
                        payload:{item: unvalidated[i],
                                field: 'errorMeaning',
                                value: errorText
                            }
                    });
                })
            } else {
                dispatch({type: 'CHANGE_STATUS',
                    payload:{item: unvalidated[i],
                            newStatus: {value: 'error', name: 'Error en metadata de archivo'}}
                });
                dispatch({type: 'CHANGE_VALUE',
                    payload:{item: unvalidated[i],
                            field: 'error',
                            value: true
                        }
                });
                dispatch({type: 'CHANGE_VALUE',
                    payload:{item: unvalidated[i],
                            field: 'errorMeaning',
                            value: "No se pudo extraer el metadata del archivo. El archivo puede estar corrupto o dañado."
                        }
                });
            }
        }
    }

    useEffect(() => {
        if(props.items.filter(item => item.status.name == "Por Validar").length) {
            validateFiles("Por Validar",'name')
        }
    });

    return (
        <>
        {current == 'error' && <ActionButton name='Validar archivos' icon={faClipboardCheck}
            action={() => validateFiles("error",'value')} statusType='error' align='45px' />}
        </>
    );
}