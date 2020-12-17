import React, { useState } from 'react';
import setHours from "date-fns/setHours";
import setMinutes from "date-fns/setMinutes";
import setSeconds from "date-fns/setSeconds";
import DatePicker from 'react-datepicker';
import classNames from 'classnames';
import exifr from 'exifr';

function Items({ idDiv, listElements, position }) {
    return (
        <ul id={idDiv} className={classNames(
                'statusDiv',
                { hidden: position >= 1 ? true : false }
            )}>
            {listElements.map((el, index) => (
                <li key={index}>
                    <p>{el.file.name}</p>
                    <input tipe="text" placeholder={el.device}/>
                    <DatePicker
                      selected={new Date(el.date)}
                      onChange={date => setStartDate(date)}
                      showTimeSelect
                      minTime={setHours(setMinutes(setSeconds(new Date(), 0), 0), 17)}
                      maxTime={setHours(setMinutes(setSeconds(new Date(), 5), 5), 20)}
                      dateFormat="dd/MM/yy h:mm:ss"
                    />
                    <p>{el.status}</p>
                </li>
            ))}
        </ul>
    )
}
class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            files: []
        }
        this.showDropZone = false;

    }

    handleFileUpload = e => {
        this.filterFilesAndDirs(e.target.files)
    }

    allowDrop = (e) => {
        document.getElementById('innerBox').setAttribute("drop-active", true);
        document.querySelector('#file + label').style.display = 'none';
        e.stopPropagation();
        e.preventDefault();
        this.showDropZone = true;
    }
    
    leaveDropZone = (e) => {
        this.showDropZone = false;
        setTimeout(() => { 
            if(!this.showDropZone) {
                document.getElementById('innerBox').removeAttribute("drop-active"); 
                document.querySelector('#file + label').style.display = 'block';
            }
        }, 200);
        
    }
    
    drop = (e) => {
        e.preventDefault();
        document.getElementById('innerBox').removeAttribute("drop-active");
        document.querySelector('#file + label').style.display = 'block';
        this.filterFilesAndDirs(e.dataTransfer.items)
    }


    filterFilesAndDirs = async (files) => {
        try {
            for (let i = 0; i < files.length; i++) {
                let file = files[i].webkitGetAsEntry();

                if(file) {
                    this.scanFiles(file, files[i]);
                }
            }
        } catch {
            for (let i = 0; i < files.length; i++) {
                this.extractData(files[i])
            }
        }
    }

    scanFiles = (item, file) => {
        if (item.isFile) {
            this.extractData(file.getAsFile())
        } else if (item.isDirectory) {
            let _this = this;
            let directoryReader = item.createReader();
            directoryReader.readEntries(entries => {
                entries.forEach(entry => {
                    entry.file(function(file) {
                        _this.extractData(file)
        			})
                });
            })
        }
    }

    extractData = async (file) => {
        if(file.type.includes('image')) {
            let exif = await exifr.parse(file)
            this.setState({ files: [...this.state.files, {
                file: file,
                device: exif.Make,
                date: exif.CreateDate.toISOString(),
                status: 'Por Validar'
            }] });
        } else {
            //let exif = await mm.parseFile(file.getAsFile());
            //console.log(exif)
            //this.setState({ files: [...this.state.files, {file: file.getAsFile(), metadata: ''}] });
        }
    }


    componentDidUpdate() {
        if (this.state.files.length) {
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
        console.log(this.state)
    }


    render() {   

        let itemStatus = [
            {
                name: 'preview',
                elements: this.state.files
            },
            {   
                name: 'uploading',
                elements: []
            },
            {
                name: 'completed',
                elements: []
            },
            {
                name: 'error',
                elements: []
            }];
        return (
            <div id="content" className="inputBox">
                <div id="innerBox" onDragOver={this.allowDrop} onDragLeave={this.leaveDropZone}
                    onDrop={this.drop}>
                    <div id="contentBox" ></div>
                    <div id="elementsList">
                        <ul id="headerList">
                            <li>
                                <p>Nombre</p>
                                <p>Dispositivo</p>
                                <p>Fecha de captura</p>
                                <p>Estado</p>
                            </li>
                        </ul>
                        {itemStatus.map((item, index) => (
                            <Items key={index} idDiv={item.name} position={index}
                                    listElements={item.elements}/>
                        ))}
                    </div>
                    <input className="inputFile" id="file" type="file" onInput={this.handleFileUpload}/>
                    <label className="inputFile" htmlFor="file"></label>
                </div>
            </div>
        )
    }

}

export default Content;