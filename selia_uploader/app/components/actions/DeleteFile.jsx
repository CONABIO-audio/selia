/** @jsx jsx */
import React from 'react';
import { css, jsx } from '@emotion/react';
import { useDispatch } from 'react-redux';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTrashAlt } from '@fortawesome/free-regular-svg-icons';

export default function DeleteFile(props) {
    const dispatch = useDispatch();

    const deleteFile = () => {
        for(let i=0;i<props.items.length;i++) {
            if (props.items[i].selected) {
                dispatch({type: 'DELETE_ITEM',
                    payload:props.items[i]
                });
                props.setFiles( props.files.filter(file => file.name !== props.items[i].file) );
            };
        }
    }

    return (
        <>
            {props.items.filter( item => item.selected).length ? 
                    <FontAwesomeIcon 
                        css={css`
                            color: white;
                            z-index: 9999;
                            position: absolute;
                            cursor: pointer;
                            top: 3px;
                        `}
                        icon={faTrashAlt} onClick={deleteFile}/> 
            : null}
        </>
    )
}