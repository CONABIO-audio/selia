/** @jsx jsx */
import React, { useEffect, useState } from 'react';
import Navbar from './elements/Navbar';
import Content from './Content';
import { css, jsx } from '@emotion/react';
import styled from '@emotion/styled';
import api from '../services/api';
import { argsAtom } from '../services/state';
import { useAtom } from 'jotai';
import ErrorMessage from './elements/ErrorMessage';

function TopInfo() {
    const [values, setValues] = useState({})
    const [args, setArgs] = useAtom(argsAtom)
    useEffect(() => {
        setValues(dataFromParams);
        let temp = {};
        Object.entries(dataFromParams).forEach(([key,value]) => {
            if(key != 'collection_metadata' && key != 'mime_types') 
                temp[key] = value[0];
            else
                temp[key] = value;
        })
        setArgs(temp);
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
                <StyledDiv>Colección: <Paragraph id="collection">{values.collection ? values.collection[1] : 'Sin colección'}</Paragraph></StyledDiv>
                <StyledDiv>Tipo de artículo: <Paragraph id="articleType">{values.item_type ? values.item_type[1] : 'Sin tipo de artículo'}</Paragraph></StyledDiv>
            </div>
            <div
                css={css`
                    width: 100%;
                    margin-top: 1.3em;
                `}
            >
                <StyledDiv>Sitio: <Paragraph id="site">{values.collection_site ? values.collection_site[1] : 'Sin sitio'}</Paragraph></StyledDiv>
                <StyledDiv>Evento de muestro: <Paragraph id="event">{values.sampling_event ? values.sampling_event[1] : 'Sin evento'}</Paragraph></StyledDiv>
                <StyledDiv>Despliegue: <Paragraph id="deploy">{values.deployment ? values.deployment[1] : 'Sin despliegue'}</Paragraph></StyledDiv>
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
            <ErrorMessage />
        </div>
    )
}
