import React, { useState } from 'react';
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
    const [currentUpload,setUpload] = useState(0);

    let i = 0;

    const checkCurrent = (action) => {
        if(action > 0) {
            setUpload(currentUpload + 1);
        } else {
            setUpload(currentUpload - 1);
        }
    }

    const upload = (fileToUpload) => {
        let onUpload = (progressEvent) => {
            var percentCompleted = Math.round( (progressEvent.loaded * 100) / progressEvent.total );
            dispatch({
                type: 'CHANGE_STATUS',
                payload:{item: fileToUpload,
                newStatus: {value: 'uploading', name: percentCompleted + '%'}}
            });
        }
        
        let file = props.files.find(file => file.name == fileToUpload.file);
        let date = new Date(fileToUpload.date)
        let validatedData = dataJson(args,date,fileToUpload);
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
            checkCurrent(-1);
            dispatch({type: 'CHANGE_STATUS',
                payload:{item: fileToUpload,
                        newStatus: {value: 'completed', 
                                    name: 'Subido', 
                                    url: window.location.origin + '/items/detail/' + resp.data.id + '/'}}
            });
        })
        .catch((err) => {
            checkCurrent(-1);
            let errorText = "";
            Object.entries(err.response.data).forEach(([key,value]) => {
                errorText = errorText + key + ": "
                errorText = errorText + value + " "
            })
            dispatch({type: 'CHANGE_STATUS',
                payload:{item: fileToUpload,
                        newStatus: {value: 'error', name: 'Error en la subida del archivo'}}
            });
            dispatch({type: 'CHANGE_VALUE',
                payload:{item: fileToUpload,
                        field: 'error',
                        value: true
                    }
            });
            dispatch({type: 'CHANGE_VALUE',
                payload:{item: fileToUpload,
                        field: 'errorMeaning',
                        value: errorText
                    }
            });
        })
    }

    const countUpload = (totalFiles, files) => {
        if(totalFiles > 0) {
            if(currentUpload < 5) {
                checkCurrent(1);
                upload(files[i]);
                totalFiles -= 1;
                i++;
                countUpload(totalFiles, files);
            } else {
                countUpload(totalFiles, files);
            }
        }
    }

    const startUpload = () => {
        let toUpload = props.items.filter(item => item.status.name == 'Validado')

        let totalFiles = toUpload.length;

        countUpload(totalFiles, toUpload);
    }

    return (
        <ActionButton name='Subir archivos' icon={faCloudUploadAlt} 
                    action={() => startUpload()} statusType='preview' align='45px' />
    )
}