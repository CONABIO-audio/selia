/** @jsx jsx */
import React from 'react';
import { css, jsx } from '@emotion/react';
import setHours from "date-fns/setHours";
import setMinutes from "date-fns/setMinutes";
import setSeconds from "date-fns/setSeconds";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import DatePicker from 'react-datepicker';
import classNames from 'classnames';

import { faCheckCircle } from '@fortawesome/free-regular-svg-icons';
import { faCircle } from '@fortawesome/free-regular-svg-icons';

import { useSelector, useDispatch } from 'react-redux';

function Items(props) {
    const items = useSelector(state => state.items.items);
    const dispatch = useDispatch();
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
        <ul id={props.idDiv} className={classNames(
                'statusDiv',
                { hidden: props.position >= 1 ? true : false }
            )}>
            {items.map((item, index) => {
                if(item.status.value == props.idDiv) {
                    return (
                        <li key={index}>
                                {item.selected ? 
                                        <FontAwesomeIcon icon={faCheckCircle} onClick={() => onClick(item)}/> : 
                                        <FontAwesomeIcon icon={faCircle} onClick={() => onClick(item)}/>}
                                <p css={css`
                                    padding-left: 10px;
                                    width: calc(20% - 10px);
                                `}>{item.file}</p>
                                <input tipe="text" placeholder={item.device} value={item.device} onChange={(e) => onChangeValue(e.target.value,item,'device')}/>
                                <DatePicker
                                  selected={new Date(item.date)}
                                  onChange={date => {setStartDate(date); onChangeValue(date, item, 'date')}}
                                  showTimeSelect
                                  minTime={setHours(setMinutes(setSeconds(new Date(), 0), 0), 17)}
                                  maxTime={setHours(setMinutes(setSeconds(new Date(), 5), 5), 20)}
                                  dateFormat="dd/MM/yy h:mm:ss"
                                />
                                <select onChange={(e) => onChangeValue(e.target.value,item,'timezoneValue')} value={item.timezoneValue}>
                                    {item.timezones.map((zone, index) => (
                                        <option key={index} value={zone}>{zone}</option>
                                    ))}
                                </select>
                                <p>{item.status ? item.status.name : null}</p>
                        </li>)
                    }
                }
            )}
        </ul>
    )
}

export default Items;