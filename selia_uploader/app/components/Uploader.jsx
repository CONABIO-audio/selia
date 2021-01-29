/** @jsx jsx */
import React, { useEffect, useState } from 'react';
import Navbar from './elements/Navbar';
import Content from './Content';
import { css, jsx } from '@emotion/react';
import styled from '@emotion/styled';
import api from '../services/api';

function TopInfo() {
    const [values, setValues] = useState({})
    useEffect(async () => {
        api.getItems().then(resp=> {
            console.log(resp)
            setValues(resp);
        })
    },[])
    const StyledDiv = styled.div`
        color: #484848;
        font-weight: bold;
    `
    const Paragraph = styled.p`
        color: gray;
        padding-left: 2em;
        font-weight: 100;
    `

    return (
        <div className="top-info">
            <div
                css={css`
                width: 100%;
                border-bottom: 4px double #b5b5b5;
              `}
            >
                <StyledDiv>Colección: <Paragraph id="collection">{values.collection ? values.collection : 'Sin colección'}</Paragraph></StyledDiv>
                <StyledDiv>Tipo de artículo: <Paragraph id="articleType">Article type example</Paragraph></StyledDiv>
                <StyledDiv>Nivel de registro: <Paragraph id="registerLevel">Register level example</Paragraph></StyledDiv>
            </div>
            <div
                css={css`
                    width: 100%;
                    margin-top: 1.3em;
                `}
            >
                <StyledDiv>Sitio: <Paragraph id="site">{values.collection_site ? values.collection_site : 'Sin sitio'}</Paragraph></StyledDiv>
                <StyledDiv>Evento de muestro: <Paragraph id="event">{values.sampling_event ? values.sampling_event : 'Sin evento'}</Paragraph></StyledDiv>
                <StyledDiv>Despliegue: <Paragraph id="deploy">{values.deployment ? values.deployment : 'Sin despliegue'}</Paragraph></StyledDiv>
                <StyledDiv>MediaInfo: <Paragraph id="media">MediaInfo example</Paragraph></StyledDiv>
                <StyledDiv>Metadatos adicionales: <Paragraph id="metadata">Metadata example</Paragraph></StyledDiv>
            </div>
        </div>
    )
}

export default function Uploader(){
    return (
        <div
            css={css`
                display: flex;
            `}
        >
            <TopInfo />
            <div
                css={css`
                    width: 80%;
                `}
            >
                <Navbar />
                <Content />
            </div>
        </div>
    )
}
