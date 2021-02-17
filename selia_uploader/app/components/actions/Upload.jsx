import React from 'react';
import { useDispatch } from 'react-redux';
import api from '../../services/api';
import ActionButton from '../elements/ActionButtons';
import { faCloudUploadAlt } from '@fortawesome/free-solid-svg-icons';


export default function Upload(props) {
    const dispatch = useDispatch();

    const uploadFiles = () => {
        let toUpload = props.items.filter(item => item.status.name == 'Validado')
        for(let i=0;i<toUpload.length;i++) {
            let percent = 0;
            let timerId = setInterval((params) => {
                percent += Math.floor(Math.random() * (20 - 1)) + 1;
                dispatch({type: 'CHANGE_STATUS',
                    payload:{item: toUpload[i],
                            newStatus: {value: 'uploading', name: percent + '%'}}
                });
                if(percent >= 100){
                    dispatch({type: 'CHANGE_STATUS',
                        payload:{item: toUpload[i],
                                newStatus: {value: 'completed', name: 'Subido'}}
                    });
                    clearInterval(timerId);
                }
            },500)
        }
    }

    return (
        <ActionButton name='Subir archivos' icon={faCloudUploadAlt} 
                    action={() => uploadFiles()} statusType='preview' align='45px' />
    )
}