/** @jsx jsx */
import React from 'react';
import { css, jsx } from '@emotion/react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import DatePicker from 'react-datepicker';
import classNames from 'classnames';

import { useAtom } from 'jotai';
import { errorMessageAtom } from '../../services/state';

import { faCheckCircle, faEye } from '@fortawesome/free-regular-svg-icons';
import { faCircle } from '@fortawesome/free-regular-svg-icons';

import { useSelector, useDispatch } from 'react-redux';

function Items(props) {
    const items = useSelector(state => state.items.items);
    const dispatch = useDispatch();
    const [message, setMessage] = useAtom(errorMessageAtom);
    const onClick = (file) => {
        dispatch({
            type: 'CHANGE_ITEM',
            payload: file
        })
    }
    const onChangeValue = (e, file, field) => {
        dispatch({
            type: 'CHANGE_VALUE',
            payload: {
                item: file,
                field: field,
                value: e
            }
        })
    }
    return (
        <ul css={css`
            height: calc(100% - ${props.idDiv == 'error' ? '9em' : '6em'})!important;
        `} id={props.idDiv} className={classNames(
                'statusDiv',
                { hidden: props.position >= 1 ? true : false }
            )}>
            {items.map((item, index) => {
                if(item.status.value == props.idDiv) {
                    return (
                        <li key={index}>
                                {(item.status.value == 'error' || item.status.value == 'preview')
                                    && <div>
                                        {item.selected ? 
                                                <FontAwesomeIcon icon={faCheckCircle} onClick={() => onClick(item)}/> : 
                                                <FontAwesomeIcon icon={faCircle} onClick={() => onClick(item)}/>}
                                    </div>}
                                <p css={css`
                                    padding-left: 10px;
                                    width: calc(20% - 10px);
                                `}>{item.file}</p>
                                <DatePicker
                                  selected={new Date(item.date)}
                                  onChange={date => {onChangeValue(date.toISOString(), item, 'date')}}
                                  showTimeSelect
                                  dateFormat="dd/MM/yy h:mm:ss"
                                />
                                <select className={"selectTimezone"} onChange={(e) => onChangeValue(e.target.value,item,'timezoneValue')} value={item.timezoneValue}>
                                    {item.timezones.map((zone, index) => (
                                        <option key={index} value={zone}>{zone}</option>
                                    ))}
                                </select>
                                {item.error ? (
                                    <div css={css`
                                        display: flex;
                                        width: 20%
                                    `}>
                                        <p css={css`
                                            width: 90%!important;
                                            margin-right: 1em!important;
                                        `}>{item.status ? item.status.name : null}</p>
                                        <button css={css`
                                        border-radius: 3px;
                                        background-color: #deebeb;
                                        color: #343a40;
                                        border: none;
                                        width: fit-content;
                                    `} onClick={() => setMessage({status: true, message: item.errorMeaning})}>?</button>
                                    </div>
                                ):
                                <p css={css`
                                    display: flex;
                                `}>
                                    {item.status ? item.status.name + ' ' : null}
                                    {(item.status && item.status.url) ? 
                                    <a css={css`
                                        color: white;
                                        display: block;
                                        padding-top: 1px;
                                        margin-left: 7px;
                                    `} href={item.status.url} target="_blank"><FontAwesomeIcon icon={faEye}/></a> : null}
                                </p>
                                }
                        </li>)
                    }
                }
            )}
        </ul>
    )
}

export default Items;