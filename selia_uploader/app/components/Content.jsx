/** @jsx jsx */
import React from 'react';
import exifr from 'exifr';
import { css, jsx } from '@emotion/react';
import Items from './Items';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import { connect } from 'react-redux';
import { addItem, deleteItem } from '../features/actions';

import { faTrashAlt } from '@fortawesome/free-regular-svg-icons';

class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            files: [],
            selected: []
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
            this.setState({ files: [...this.state.files, file] });
            this.props.addItem(
                {
                    file: file.name,
                    device: exif.Make,
                    date: exif.CreateDate.toISOString(),
                    status: {
                        value: 'preview',
                        name: 'Por Validar'
                    },
                    selected: false
                }
            )
        } else {
            this.setState({ files: [...this.state.files, file] });
            this.props.addItem(
                {
                    file: file.name,
                    device: 'No especificado',
                    date: new Date().toLocaleDateString(),
                    status: {
                        value: 'preview',
                        name: 'Por Validar'
                    },
                    selected: false
                }
            )
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

    delete = () => {
        for(let i=0;i<this.props.items.length;i++) {
            if (this.props.items[i].selected) {
                this.props.deleteItem(this.props.items[i]);
                this.setState({ files: this.state.files.filter(file => file.name !== this.props.items[i].file) });
            };
        }
    }

    render() {
        let itemStatus = ['preview','uploading','completed','error'];
        return (
            <div id="content" className="inputBox">
                <div id="innerBox" onDragOver={this.allowDrop} onDragLeave={this.leaveDropZone}
                    onDrop={this.drop}>
                    <div id="contentBox" ></div>
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
                        {itemStatus.map((item, index) => (
                            <Items key={index} idDiv={item} position={index} />
                        ))}
                    </div>
                    <input className="inputFile" id="file" type="file" onInput={this.handleFileUpload}/>
                    <label className="inputFile" htmlFor="file"></label>
                    {this.props.items.filter( item => item.selected).length ? 
                            <FontAwesomeIcon 
                                css={css`
                                    color: white;
                                    z-index: 9999;
                                    position: absolute;
                                    cursor: pointer;
                                    top: 3px;
                                `}
                                icon={faTrashAlt} onClick={() => this.delete()}/> 
                    : null}
                </div>
            </div>
        )
    }

}

const mapStateToProps = state => {
    return { items: state.items.items };
}

const mapDispatchToProps = dispatch => {
    return { 
        addItem: item => dispatch(addItem(item)),
        deleteItem: item => dispatch(deleteItem(item))
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(Content)