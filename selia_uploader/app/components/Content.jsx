/** @jsx jsx */
import React, { useState, useEffect } from 'react';
import exifr from 'exifr';
import { css, jsx } from '@emotion/react';
import Items from './Items';
import ActionButton from './ActionButtons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import api from '../services/api';

import { useSelector, useDispatch } from 'react-redux';

import { faTrashAlt } from '@fortawesome/free-regular-svg-icons';
import { faClipboardCheck, faCoins } from '@fortawesome/free-solid-svg-icons';
import { faCloudUploadAlt } from '@fortawesome/free-solid-svg-icons';

function Content(){
    const [files, setFiles] = useState([])
    let showDropZone = false;

    const items = useSelector(state => state.items.items);
    const dispatch = useDispatch();

    const handleFileUpload = e => {
        filterFilesAndDirs(e.target.files)
    }

    const allowDrop = (e) => {
        document.getElementById('innerBox').setAttribute("drop-active", true);
        document.querySelector('#file + label').style.display = 'none';
        e.stopPropagation();
        e.preventDefault();
        showDropZone = true;
    }
    
     const leaveDropZone = (e) => {
        showDropZone = false;
        setTimeout(() => { 
            if(!showDropZone) {
                document.getElementById('innerBox').removeAttribute("drop-active"); 
                document.querySelector('#file + label').style.display = 'block';
            }
        }, 200);
        
    }
    
    const drop = (e) => {
        e.preventDefault();
        document.getElementById('innerBox').removeAttribute("drop-active");
        document.querySelector('#file + label').style.display = 'block';
        filterFilesAndDirs(e.dataTransfer.items)
    }


    const filterFilesAndDirs = async (files) => {
        try {
            for (let i = 0; i < files.length; i++) {
                let file = files[i].webkitGetAsEntry();

                if(file) {
                    scanFiles(file, files[i]);
                }
            }
        } catch {
            for (let i = 0; i < files.length; i++) {
                extractData(files[i])
            }
        }
    }

    const scanFiles = (item, file) => {
        if (item.isFile) {
            extractData(file.getAsFile())
        } else if (item.isDirectory) {
            let directoryReader = item.createReader();
            directoryReader.readEntries(entries => {
                entries.forEach(entry => {
                    entry.file(function(file) {
                        extractData(file)
        			})
                });
            })
        }
    }

    const extractData = async (file) => {
        if(file.type.includes('image')) {
            let exif = await exifr.parse(file)
            setFiles( [...files, file] );
            dispatch({type: 'ADD_ITEM',
                payload: {
                    file: file.name,
                    device: exif.Make,
                    date: exif.CreateDate ? exif.CreateDate.toISOString() : new Date().toISOString(),
                    status: {
                        value: 'preview',
                        name: 'Por Validar'
                    },
                    selected: false
                }
            })
        } else {
            setFiles( [...files, file] );
            dispatch({type: 'ADD_ITEM',
                payload:{
                    file: file.name,
                    device: 'No especificado',
                    date: new Date().toLocaleDateString(),
                    status: {
                        value: 'preview',
                        name: 'Por Validar'
                    },
                    selected: false
                }
            })
        }
    }

    useEffect(() => {
        if (files.length) {
            document
                .getElementById("file")
                .labels[0].setAttribute("enable-button", true);
            document.getElementById("contentBox").setAttribute("drop-hidden", true);
            document.getElementById("elementsList").style.display = "block";
        } else {
            document.getElementById("file").labels[0].removeAttribute("enable-button");
            document.getElementById("contentBox").removeAttribute("drop-hidden");
            document.getElementById("elementsList").style.display = "none";
        }
    })

    const deleteFile = () => {
        for(let i=0;i<items.length;i++) {
            if (items[i].selected) {
                dispatch({type: 'DELETE_ITEM',
                    payload:items[i]
                });
                setFiles( files.filter(file => file.name !== items[i].file) );
            };
        }
    }

    const validateFiles = () => {
        for(let i=0;i<items.length;i++) {
            let date = new Date(items[i].date)
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
                "captured_on_timezone": "",
                "media_info": { "image_width": 200, "image_length": 200, "datetime_original": date.toISOString() },
                "collection": 2,
                "sampling_event": 1135,
                "collection_device": 15,
                "collection_site": 989,
                "deployment": 595,
                "collection_metadata": '',
                "mime_type": 50
            }
            api.validate(data).then((resp) => {
                dispatch({type: 'CHANGE_STATUS',
                    payload:{item: items[i],
                            newStatus: {value: 'preview', name: 'Validado'}}
                });
            })
            .catch(err => {
                console.log(err)
                dispatch({type: 'CHANGE_STATUS',
                    payload:{item: items[i],
                            newStatus: {value: 'error', name: 'Error en validacion'}}
                });
            })
        }
    }

    let itemStatus = ['preview','uploading','completed','error'];
    return (
        <div id="content" className="inputBox" css={css`position: relative`}>
            <div id="innerBox" onDragOver={allowDrop} onDragLeave={leaveDropZone}
                onDrop={drop}>
                <div id="contentBox"></div>
                <div id="elementsList">
                    <ul id="headerList">
                        <li>
                            <p css={css`width: 15px!important;`}></p>
                            <p>Nombre</p>
                            <p>Dispositivo</p>
                            <p>Fecha de captura</p>
                            <p>Estado</p>
                        </li>
                    </ul>
                    {itemStatus.map((title, index) => (
                        <Items key={index} idDiv={title} position={index} />
                    ))}
                </div>
                <input className="inputFile" id="file" type="file" onInput={handleFileUpload}/>
                <label className="inputFile" htmlFor="file"></label>
                {items.filter( item => item.selected).length ? 
                        <FontAwesomeIcon 
                            css={css`
                                color: white;
                                z-index: 9999;
                                position: absolute;
                                cursor: pointer;
                                top: 3px;
                            `}
                            icon={faTrashAlt} onClick={() => deleteFile()}/> 
                : null}
            </div>
            {items.length ? 
            (<>
                <ActionButton name='Validar archivos' icon={faClipboardCheck} 
                    action={() => validateFiles()} statusType='Por Validar' align='210px' />
                <ActionButton name='Subir archivos' icon={faCloudUploadAlt} 
                    action={() => validateFiles()} statusType='Validado' align='45px' />
            </>) : null}
        </div>
    )

}

export default Content;