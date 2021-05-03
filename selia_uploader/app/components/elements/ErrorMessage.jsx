/** @jsx jsx */
import { css, jsx } from '@emotion/react'
import React from 'react';
import { useAtom } from 'jotai';
import { errorMessageAtom } from '../../services/state';

export default function ErrorMessage() {
    const [show,setShow] = useAtom(errorMessageAtom);
    return (
        <div css={css`
            display: ${show.status ? 'block' : 'none'};
            position: absolute;
            width: 100%;
            height: 100%;
            z-index: 9999;
        `}>
            <div css={css`
                padding: 2em;
                border-radius: 4px;
                background-color: #dfecec;
                color: #343a40;
                width: 40%;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%,-50%);
            `}>
                <button css={css`
                    position: absolute;
                    right: 5px;
                    top: 5px;
                    background: transparent;
                    color: #343a40;
                    border: none;
                    font-weight: 800;
                    font-size: 20px;
                `} onClick={() => setShow({status: false, message: ''})}>x</button>
                <h4>Error:</h4>
                <p>{show.message}</p>
            </div>
            <div css={css`
                width: 100%;
                height: 100%;
                background-color: #0000008c;
            `} onClick={() => setShow({status: false, message: ''})}></div>
        </div>
    )
}