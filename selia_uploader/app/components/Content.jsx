/** @jsx jsx */
import React, { useEffect } from 'react';
import exifr from 'exifr';
import { css, jsx } from '@emotion/react';
import Items from './elements/Items';
import ActionButton from './elements/ActionButtons';
import Validate from './actions/Validate';
import DeleteFiles from './actions/DeleteFile';
import timezones from '../services/timezones';

import { useSelector, useDispatch } from 'react-redux';
import { useAtom } from 'jotai';
import { fileAtom } from '../services/state';

import { faCloudUploadAlt } from '@fortawesome/free-solid-svg-icons';

function Content(){
    const [files, setFiles] = useAtom(fileAtom)
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
            ExtractFileData.extractData(file.getAsFile())
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
            let date = exif.CreateDate ? exif.CreateDate.toISOString() : new Date().toISOString()
            let timezone = timezones.getTimeZones(date)
            setFiles( [...files, file] );
            dispatch({type: 'ADD_ITEM',
                payload: {
                    file: file.name,
                    device: exif.Make,
                    date: date,
                    timezones: timezone,
                    timezoneValue: timezone[0],
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
                            <p>Zona horaria</p>
                            <p>Estado</p>
                        </li>
                    </ul>
                    {itemStatus.map((title, index) => (
                        <Items key={index} idDiv={title} position={index} />
                    ))}
                </div>
                <input className="inputFile" id="file" type="file" onInput={handleFileUpload}/>
                <label className="inputFile" htmlFor="file"></label>
                <DeleteFiles items={items} files={files} setFiles={setFiles} />
            </div>
            {items.length ? 
            (<>
                <Validate items={items}/>
                <ActionButton name='Subir archivos' icon={faCloudUploadAlt} 
                    action={() => validateFiles()} statusType='Validado' align='45px' />
            </>) : null}
        </div>
    )

}

export default Content;