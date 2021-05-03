/** @jsx jsx */
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { css, jsx } from '@emotion/react';
import { useSelector } from 'react-redux';

function ActionButton(props) {
    const items = useSelector(state => state.items.items);
    
    return (
        <div className="checkFile actionButton" css={css`
        pointer-events: ${items.filter(item => 
            item.status.value == props.statusType).length ? 'initial' : 'none'};
        color: ${items.filter(item => 
                item.status.value == props.statusType).length ? '#f8f8f3;' : '#828282;'}
        right: ${props.align};`} onClick={props.action}>
            <div css={css`
                font-size: 1.4em;`}>
                <FontAwesomeIcon icon={props.icon}/>
            </div>
            <div css={css`
            padding: 0 0px 0 10px;
            line-height: 34px;
            font-weight: 900;
            font-size: 14px;`}>{props.name}</div>
        </div>
    )
}

export default ActionButton;