/** @jsx jsx */
import React, { useEffect, useState } from 'react';
import { css, jsx } from '@emotion/react';
import Items from './elements/Items';
import Validate from './actions/Validate';
import Upload from './actions/Upload';
import AlterInfo from './actions/AlterInfo';
import DeleteFiles from './actions/DeleteFile';
import timezones from '../services/timezones';
import mediaInfo from '../services/mediaInfo';

import { useSelector, useDispatch } from 'react-redux';
import { useAtom } from 'jotai';
import { argsAtom, currentDivAtom } from '../services/state';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons'

function Content(){
    const [files, setFiles] = useState([])
    const [badFileType, setWarningFileType] = useState([false,''])
    const [args, setArgs] = useAtom(argsAtom)
    const [current] = useAtom(currentDivAtom)
    const [showLoading,setLoading] = useState('none');
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

    const filterFilesAndDirs = (items) => {
        try {
            setLoading('block');
            let filesArray = [];
            for (let i = 0; i < items.length; i++) {
                let file = items[i].webkitGetAsEntry();

                if(file) {
                    let fileOrFiles = scanFiles(file, items[i]);
                    if (typeof fileOrFiles.length != 'undefined') {
                        for(let j=0;j<fileOrFiles.length;j++) {
                            filesArray.push(fileOrFiles[i]);
                        }
                    } else {
                        filesArray.push(fileOrFiles)
                    }
                }
            }
            setFiles(files.concat(filesArray));
        } catch {
            let filesArray = [];
            for (let i = 0; i < items.length; i++) {
                if(args.mime_types.find(type => type[1] == items[i].type.replace("audio/wav","audio/x-wav"))) {
                    extractData(items[i])
                    filesArray.push(items[i])
                    setWarningFileType([false,''])
                } else {
                    let types = args.mime_types.map(type => type[1])
                    setWarningFileType([true,'Se esparaba un archivo de tipo ' + types + ' y se obtuvo un archivo de tipo ' + items[i].type])
                }
            }
            setFiles(files.concat(filesArray));
        }
    }
    const scanFiles = (item, file) => {
        if (item.isFile) {
            if(args.mime_types.find(type => type[1] == file.type.replace("audio/wav","audio/x-wav"))) {
                extractData(file.getAsFile())
                setWarningFileType([false,''])
                return file.getAsFile()
            } else {
                let types = args.mime_types.map(type => type[1])
                setWarningFileType([true,'Se esparaba un archivo de tipo ' + types + ' y se obtuvo un archivo de tipo ' + file.type])
            }
        } else if (item.isDirectory) {
            let directoryReader = item.createReader();
            let fileArray = [];
            directoryReader.readEntries(entries => {
                entries.forEach(entry => {
                    entry.file(function(file) {
                        if(args.mime_types.find(type => type[1] == file.type.replace("audio/wav","audio/x-wav"))){
                            extractData(file);
                            fileArray.push(file);
                        }
                    })
                });
            })
            return fileArray;
        }
    }

    const extractData = (file) => {
        mediaInfo.getMediaInfo(file).then(metadata => { 
            if(file.type.includes('image')) {
                let timezone = timezones.getTimeZones(metadata[1])
                dispatch({type: 'ADD_ITEM',
                    payload: {
                        file: file.name,
                        type: file.type,
                        date: metadata[1],
                        timezones: timezone,
                        timezoneValue: timezone[0],
                        metadata: metadata[0],
                        status: {
                            value: 'preview',
                            name: 'Por Validar'
                        },
                        selected: false
                    }
                })
            } else {
                let date = new Date().toISOString()
                let timezone = timezones.getTimeZones(date)
                dispatch({type: 'ADD_ITEM',
                    payload:{
                        file: file.name,
                        date: date,
                        type: file.type,
                        timezones: timezone,
                        timezoneValue: timezone[0],
                        metadata: metadata,
                        status: {
                            value: 'preview',
                            name: 'Por Validar'
                        },
                        selected: false
                    }
                })
            }
        })
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
        if(files.length == items.length) {
            setLoading('none');
        }
    })

    let itemStatus = ['preview','uploading','completed','error'];
    return (
        <div id="content" className="inputBox" css={css`position: relative`}>
            <div className={"loadingFiles"} css={css`
                position: absolute;
                color: white;
                width: 95%;
                height: 95%;
                border-radius: 3px;
                background: #262b2fb8;
                z-index: 999999;
                display: ${showLoading};
            `}></div>
            <div id="innerBox" onDragOver={allowDrop} onDragLeave={leaveDropZone}
                onDrop={drop}>
                <div id="contentBox"></div>
                <div id="elementsList">
                    <ul id="headerList">
                        <li>
                            <p css={css`width: 15px!important;`}></p>
                            <p css={css`
                                    padding-left: 10px;
                                    width: calc(20% - 10px);
                                `}>Nombre</p>
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
            <div css={css`
                display: ${badFileType[0] ? 'block' : 'none'};
                position: absolute;
                bottom: 0.7em;
                left: 50%;
                transform: translateX(-50%);
                color: white;
                text-align: center;
            `}>
                <FontAwesomeIcon icon={faExclamationTriangle}/> Tipo de archivo incompatible
                <p css={css`    
                    margin: 0;
                    font-size: 14px;
                    margin-top: 5px;
                `}
                >{badFileType[1]}</p>
            </div>
            {items.length ? 
            (<> 
                {current == 'error' && <AlterInfo items={items} />}
                <Validate items={items}/>
                {current == 'preview' && <Upload items={items} />}
            </>) : null}
        </div>
    )

}

export const hasClass = (idOrClass,className) => {
    return document.querySelector(idOrClass).classList.contains(className);
}

export default Content;