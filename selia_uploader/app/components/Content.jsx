import React from 'react';
import classNames from 'classnames';

function Items({ idDiv, listElements, position }) {
    return (
        <ul id={idDiv} className={classNames(
                'statusDiv',
                { hidden: position >= 1 ? true : false }
            )}>
            {listElements.map((el, index) => (
                <li key={index}>
                    <p>{el.name}</p>
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
    }

    handleFileUpload = e => {
        if (e.target.files[0]) this.setState({ files: [...this.state.files, e.target.files[0]] });
    }

    allowDrop = (e) => {
        e.target.parentElement.setAttribute("drop-active", true);
        e.stopPropagation();
        e.preventDefault();
    }
    
    leaveDropZone = (e) => {
        e.target.parentElement.removeAttribute("drop-active");
    }
    
    drop = (e) => {
        e.preventDefault();
        e.target.parentElement.removeAttribute("drop-active");
        this.filterFilesAndDirs(e.dataTransfer.items)
    }


    filterFilesAndDirs = (files) => {
        try {
            for (let i = 0; i < files.length; i++) {
                let file = files[i].webkitGetAsEntry();

                if(file) {
                    this.scanFiles(file, files[i]);
                }
            }
        } catch {
            for (let i = 0; i < files.length; i++) {
                if (files[i].type) { // if it has mimetype, is a file
                    this.setState({ files: [...this.state.files, files[i]] });
                } else {
                    // if not, maybe a unknown file or dir
                    try { // check first bytes of file, if error then is a directory 
                        new FileReader().readAsBinaryString(files[i].slice(0, 5));
                    
                        this.setState({ files: [...this.state.files, files[i]] });// if no exception is definitely a file
                    } catch ( e ) {
                    
                    }
                }
            }
        }
    }


    scanFiles = (item, file) => {
        if (item.isFile) {
            this.setState({ files: [...this.state.files, file.getAsFile()] });
        } else if (item.isDirectory) {
            let _this = this;
            let directoryReader = item.createReader();
            directoryReader.readEntries(entries => {
                entries.forEach(entry => {
                    entry.file(function(file) {
                        _this.setState({ files: [..._this.state.files, file] });
        			})
                });
            })
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
    }

    render() {    
        let itemStatus = [
            {
                name: 'preview',
                elements: this.state.files
            },
            {   
                name: 'uploading',
                elements: ['item1']
            },
            {
                name: 'completed',
                elements: ['item2']
            },
            {
                name: 'error',
                elements: ['item3']
            }];
        return (
            <div id="content" className="inputBox">
                <div id="innerBox">
                    <div id="contentBox" onDragOver={this.allowDrop} onDragLeave={this.leaveDropZone}
                    onDrop={this.drop}></div>
                    <div id="elementsList">
                        <ul id="headerList">
                            <li>
                                <p>Nombre</p>
                                <p>Sitio</p>
                                <p>Dispositivo</p>
                                <p>Evento de muestreo</p>
                                <p>Despliegue</p>
                                <p>Fecha de captura</p>
                                <p>MediaInfo</p>
                                <p>Metadatos adicionales</p>
                                <p>Estado</p>
                            </li>
                        </ul>
                        {itemStatus.map((item, index) => (
                            <Items key={index} idDiv={item.name} position={index}
                                    listElements={item.elements}/>
                        ))}
                    </div>
                    <input className="inputFile" id="file" type="file"/>
                    <label className="inputFile" htmlFor="file" onDragOver={this.allowDrop} onDragLeave={this.leaveDropZone}
                        onDrop={this.drop}></label>
                </div>
            </div>
        )
    }

}

export default Content;