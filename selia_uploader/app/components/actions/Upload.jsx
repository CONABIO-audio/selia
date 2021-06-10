import React from 'react';
import { useDispatch } from 'react-redux';
import api from '../../services/api';
import ActionButton from '../elements/ActionButtons';
import { dataJson } from './Validate'; 
import { faCloudUploadAlt } from '@fortawesome/free-solid-svg-icons';
import { argsAtom } from '../../services/state';
import { useAtom } from 'jotai';


export default function Upload(props) {
    const dispatch = useDispatch();
    const [args] = useAtom(argsAtom)

    const uploadFiles = () => {
        let toUpload = props.items.filter(item => item.status.name == 'Validado')
        for(let i=0;i<toUpload.length;i++) {
            let onUpload = (progressEvent) => {
                var percentCompleted = Math.round( (progressEvent.loaded * 100) / progressEvent.total );
                dispatch({
                    type: 'CHANGE_STATUS',
                    payload:{item: toUpload[i],
                    newStatus: {value: 'uploading', name: percentCompleted + '%'}}
                });
            }
            
            let file = props.files.find(file => file.name == toUpload[i].file);
            let date = new Date(toUpload[i].date)
            let validatedData = dataJson(args,date,toUpload[i]);
            let data = new FormData();

            data.append('item_file',file)
            Object.entries(validatedData).forEach(([key,value]) => {
                if(value)
                    if(key.includes('media_info'))
                        data.append(key,JSON.stringify(value))
                    else
                        data.append(key,value)
            })
            api.upload(data,onUpload).then((resp) => {
                dispatch({type: 'CHANGE_STATUS',
                    payload:{item: toUpload[i],
                            newStatus: {value: 'completed', 
                                        name: 'Subido', 
                                        url: window.location.origin + '/items/detail/' + resp.data.id + '/'}}
                });
            })
            .catch((err) => {
                let errorText = "";
                Object.entries(err.response.data).forEach(([key,value]) => {
                    errorText = errorText + key + ": "
                    errorText = errorText + value + " "
                })
                dispatch({type: 'CHANGE_STATUS',
                    payload:{item: toUpload[i],
                            newStatus: {value: 'error', name: 'Error en la subida del archivo'}}
                });
                dispatch({type: 'CHANGE_VALUE',
                    payload:{item: toUpload[i],
                            field: 'error',
                            value: true
                        }
                });
                dispatch({type: 'CHANGE_VALUE',
                    payload:{item: toUpload[i],
                            field: 'errorMeaning',
                            value: errorText
                        }
                });
            })
        }
    }

    return (
        <ActionButton name='Subir archivos' icon={faCloudUploadAlt} 
                    action={() => uploadFiles()} statusType='preview' align='45px' />
    )
}