/** @jsx jsx */
import React from 'react';
import Navbar from './Navbar';
import Content from './Content';
import { css, jsx } from '@emotion/react';
import styled from '@emotion/styled';

function TopInfo() {
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
                <StyledDiv>Colección: <Paragraph id="collection">Collection example</Paragraph></StyledDiv>
                <StyledDiv>Tipo de artículo: <Paragraph id="articleType">Article type example</Paragraph></StyledDiv>
                <StyledDiv>Nivel de registro: <Paragraph id="registerLevel">Register level example</Paragraph></StyledDiv>
            </div>
            <div
                css={css`
                    width: 100%;
                    margin-top: 1.3em;
                `}
            >
                <StyledDiv>Sitio: <Paragraph id="site">Site example</Paragraph></StyledDiv>
                <StyledDiv>Evento de muestro: <Paragraph id="event">Event example</Paragraph></StyledDiv>
                <StyledDiv>Despliegue: <Paragraph id="deploy">Deploy example</Paragraph></StyledDiv>
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
