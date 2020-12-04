import React from 'react';
import Navbar from './Navbar';
import Content from './Content';

function TopInfo() {
    return (
        <div className="top-info">
            <div id="leftInfo">
                <input placeholder="Coleccion" />
                <input placeholder="Tipo de artículo" />
                <input placeholder="Nivel de registro" />
            </div>
            <div id="rightInfo">
                Información contextual
            </div>
        </div>
    )
}

export default function Uploader(){
    return (
        <>
            <TopInfo />
            <Navbar />
            <Content />
        </>
    )
}
